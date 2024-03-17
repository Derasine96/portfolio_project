from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.tag import Tag, TagBase
from models.diary import DiaryEntry, DiaryBase
from .database import get_db

router = APIRouter()


@router.post("/tags", response_model=Tag)
async def create_tag(tag_base: TagBase, db: Session = Depends(get_db)):
    """Create a new tag"""
    existing_tag = db.query(Tag).filter_by(name=tag_base.name).first()
    if existing_tag:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="A tag with this name already exists.")
    new_tag = Tag(**tag_base.dict())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@router.get("/tags/{tag_name}", response_model=Tag)
def read_tag(tag_name: TagBase, db: Session = Depends(get_db)):
    """Get a specific tag by name."""
    tag = db.query(Tag).filter_by(name=tag_name).first()
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found")
    return tag


@router.delete("/tags/{tag_name}")
def delete_tag(tag_name: TagBase, db: Session = Depends(get_db)):
    """Delete a tag by name."""
    tag = db.query(Tag).filter_by(name=tag_name).first()
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found")
    db.delete(tag)
    db.commit()


@router.put("/tags/{tag_name}", response_model=Tag)
def update_tag(tag_name: str, tag: TagBase, db: Session = Depends(get_db)):
    """Update a Tag with a diary entry"""
    existing_tag = db.query(Tag).filter_by(name=tag_name).first()
    if existing_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    for field, value in tag.dict().items():
        setattr(existing_tag, field, value)
    try:
        db.commit()
        db.refresh(existing_tag)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to update tag in the database") from e
    return existing_tag
