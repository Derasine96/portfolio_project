from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from typing import Optional
from .tag import diary_tags


class DiaryEntry(Base):
    """Create table for diary creation"""
    __tablename__ = 'diary_entries'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), nullable=False)
    entry = Column(String(2000), nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    authorId = Column(Integer, ForeignKey('users.id'), nullable=False)
    tags = relationship("Tag", secondary=diary_tags,
                        back_populates="diary_entries")


class DiaryBase(BaseModel):
    """Validator for request from database"""
    title: str
    entry: str
    authorId: int
    createdAt: str
    tag_id: Optional[int] = None


class ReadDiary(BaseModel):
    """Validator for request from database"""
    title: str
    createdAt: str
    entry: str
    authorId: int
    tag_id: Optional[int] = None
