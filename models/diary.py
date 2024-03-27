from typing import Optional
from sqlalchemy import Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from .tag import diary_tags

class DiaryEntry(Base):
    """Create table for diary creation"""
    __tablename__ = 'diary_entries'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), nullable=False)
    entry = Column(String(2000), nullable=False)
    createdAt = Column(Date, nullable=False, server_default=func.now())
    authorId = Column(Integer, ForeignKey('users.id'), nullable=False)
    tags = relationship("Tag", secondary=diary_tags,
                        back_populates="diary_entries")


class CreateDiary(BaseModel):
    """Validator for request from database"""
    title: Optional[str]
    entry: str
    tag_name: Optional[str] = None


class DiaryBase(BaseModel):
    """Validator for request from database"""
    id: int
    title: str
    entry: str
    tag_name: Optional[str] = None


class ReadDiary(BaseModel):
    """Validator for request from database"""
    id: int
    title: Optional[str]
    createdAt: str
    entry: str
