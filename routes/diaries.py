from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.diary import DiaryEntry, DiaryBase
from models.tag import Tag
from database import get_db
from routes.users import get_user
from models.user import User
from typing import Optional


router = APIRouter(prefix="/diaries", tags=["Diaries"])


@router.post("/diary", response_model=DiaryBase)
async def create_diary(diary: DiaryBase, db: Session = Depends(get_db)):
    """Create new diary item"""
    user = await get_user(User.username, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_diary = DiaryEntry(
        title=diary.title,
        entry=diary.entry,
        authorId=user.id
    )
    if diary.tag_name:
        tag = db.query(Tag).filter(Tag.name == diary.tag_name).first()
        if tag is None:
            tag = Tag(name=diary.tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        new_diary.tags.append(tag)
    try:
        db.add(new_diary)
        db.commit()
        db.refresh(new_diary)
    except SQLAlchemyError as e:
        print(f"Error occurred while adding diary: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error occurred") from e
    return new_diary


@router.get("/diary", response_model=list[DiaryBase])
async def get_diary_entries(page: int = Query(1, gt=0),
                            page_size: int = Query(10, gt=0), db: Session = Depends(get_db)
                            ):
    """Retrieve paginated diary entries."""
    offset = (page - 1) * page_size
    diary_entries = db.query(DiaryEntry).offset(offset).limit(page_size).all()
    return diary_entries


@router.get("/diary/{diary_name}", response_model=DiaryBase)
def read_diary(diary_name: str, db: Session = Depends(get_db)):
    """Get an existing diary by title."""
    diary = db.query(DiaryEntry).filter(DiaryEntry.title == diary_name).first()
    if not diary:
        raise HTTPException(status_code=404,
                            detail="Diary does not exist")
    return diary


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
