import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.quote import Quote, QuoteBase

router = APIRouter()


@router.get("/quote", response_model=QuoteBase)
async def get_random_quote(db: Session = Depends(get_db)):
    """Route to get random quotes"""
    url = "https://api.quotable.io/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        quote_text = data.get("content", "")
        author = data.get("author", "")
        max_quote_length = 1000
        quote_text = quote_text[:max_quote_length]
        if quote_text and author:
            quote = Quote(quote=quote_text, author=author)
            db.add(quote)
            db.commit()
            return {"quote": quote_text, "author": author}
    return {"detail": "Failed to fetch quote"}
