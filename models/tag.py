from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from database import Base

diary_tags = Table('diary_tags', Base.metadata,
                   Column('diary_id', Integer, ForeignKey('diary_entries.id')),
                   Column('tag_id', Integer, ForeignKey('tags.id'))
                   )


class Tag(Base):
    """Model to represent tags."""
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    diary_entries = relationship(
        "DiaryEntry", secondary=diary_tags, back_populates="tags")


class TagBase(BaseModel):
    """Validator for request from database"""
    name: str
