from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

diary_tags = Table('diary_tags', Base.metadata,
    Column('diary_id', Integer, ForeignKey('diary_entries.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class DiaryEntry(Base):
    """Create table for diary creation"""
    __tablename__ = 'diary_entries'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), nullable=False)
    entry = Column(String(2000), nullable=False)
    createdAt = Column(Date, nullable=False,
                       server_default="CURRENT_TIMESTAMP")
    authorId = Column(Integer, ForeignKey('users.id'), nullable=False)
    tags = relationship("Tag", secondary=diary_tags,
                        back_populates="diary_entries")

class DiaryBase(BaseModel):
    """Validator for request from database"""
    title: str
    entry: str
    authorId: int
    createdAt: str

class ReadDiary(BaseModel):
    """Validator for request from database"""
    title: str
    createdAt: str
