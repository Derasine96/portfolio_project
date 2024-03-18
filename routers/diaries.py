from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.diary import DiaryEntry, DiaryBase
from models.tag import TagBase, Tag
from database import get_db

router = APIRouter(prefix="/diaries", tags=["Diaries"])


@router.post("/diary", response_model=DiaryBase)
async def create_diary(diary: DiaryBase, db: Session = Depends(get_db)):
    """Create new diary item"""
    new_diary = DiaryEntry(
        title=diary.title, content=diary.content, date=diary.date, tag_id=diary.tag_id)
    try:
        db.add(new_diary)
        db.commit()
        db.refresh(new_diary)
    except SQLAlchemyError as e:
        print(f"Error occurred while adding diary: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error occurred") from e
    return new_diary


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
                       tag_name: str, db: Session = Depends(get_db)):
    """Update an existing diary by title."""
    existing_diary = db.query(DiaryEntry).filter_by(title=diary_name).first()
    if not existing_diary:
        raise HTTPException(status_code=404,
                            detail="Diary does not exist")
    existing_diary.title = diary_update.title
    existing_diary.content = diary_update.content
    existing_diary.date = diary_update.date
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
