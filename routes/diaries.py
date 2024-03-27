from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.diary import DiaryEntry, DiaryBase, ReadDiary, CreateDiary
from models.tag import Tag
from database import get_db
from routes.users import User
from models.user import User
from typing import Optional
from typing import List

router = APIRouter(prefix="/diaries", tags=["Diaries"])


@router.post("/diary", response_model=CreateDiary)
async def create_diary(diary: CreateDiary, user_name: str, db: Session = Depends(get_db)):
    """Create new diary item"""
    user = db.query(User).filter(User.username == user_name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_diary = DiaryEntry(
        title=diary.title,
        entry=diary.entry,
        authorId=user.id
    )
    try:
        db.add(new_diary)
        db.commit()
        db.refresh(new_diary)
        if diary.tag_name:
            tag = db.query(Tag).filter(Tag.name == diary.tag_name).first()
            if tag is None:
                tag = Tag(name=diary.tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            new_diary.tags.append(tag)  # Moved inside the if block
    except SQLAlchemyError as e:
        print(f"Error occurred while adding diary: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error occurred") from e
    return new_diary


@router.get("/diary", response_model=List[ReadDiary])
async def get_diary_entries_by_title_and_tag(
    title: str = Query(None),
    tag: str = Query(None),
    db: Session = Depends(get_db)
):
    """Retrieve diary entries by title and/or tag."""
    if title and tag:
        diary_entries = db.query(DiaryEntry).filter(
            DiaryEntry.title == title, DiaryEntry.tags.any(text(tag))
        ).all()
    elif title:
        diary_entries = db.query(DiaryEntry).filter_by(title=title).all()
    elif tag:
        diary_entries = db.query(DiaryEntry).filter(
            DiaryEntry.tags.any(tag)).all()
    else:
        diary_entries = db.query(DiaryEntry).all()
    return diary_entries


@router.get("/diary/{diary_name}", response_model=ReadDiary)
def read_diary(diary_name: str, db: Session = Depends(get_db)):
    """Get an existing diary by title."""
    diary = db.query(DiaryEntry).filter(DiaryEntry.title == diary_name).first()
    if not diary:
        raise HTTPException(status_code=404, detail="Diary does not exist")
    tags = db.query(Tag).filter(Tag.name == diary.title).all()
    return {
        "id": diary.id,
        "title": diary.title,
        "entry": diary.entry,
        "createdAt": diary.createdAt.isoformat(),
        "tags": tags
    }


@router.put("/diary/{diary_name}", response_model=DiaryBase)
async def update_diary(diary_name: str, diary_update: DiaryBase,
                       tag_name: Optional[str], db: Session = Depends(get_db)):
    """Update an existing diary by title."""
    existing_diary = db.query(DiaryEntry).filter_by(title=diary_name).first()
    if not existing_diary:
        raise HTTPException(status_code=404,
                            detail="Diary does not exist")
    existing_diary.title = diary_update.title
    existing_diary.entry = diary_update.entry
    if tag_name:
        tag = db.query(Tag).filter_by(name=tag_name).first()
        if not tag:
            raise HTTPException(status_code=404,
                                detail=f"Tag '{tag_name}' does not exist")
        existing_diary.tags.append(tag)
    db.commit()
    return existing_diary


@router.delete("/diary/{diary_name}", response_model=DiaryBase)
async def delete_diary(diary_name: str, db: Session = Depends(get_db)):
    """Delete a diary entry by title"""
    existing_diary = db.query(DiaryEntry).filter_by(title=diary_name).first()
    if not existing_diary:
        raise HTTPException(status_code=404,
                            detail="Diary does not exist")
    db.delete(existing_diary)
    db.commit()
