from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    quote = Column(String(1000), index=True)
    author = Column(String(50))


class QuoteBase(BaseModel):
    """Validator for request from database"""
    quote: str
    author: str