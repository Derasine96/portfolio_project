from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.user import User, UserBase
from .database import get_db
from passlib.hash import bcrypt

router = APIRouter()

@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    """Add a new user to the users table"""
    if not user.username:
        raise HTTPException(status_code=400, detail="Username is required")
    if not user.password:
        raise HTTPException(status_code=400, detail="Password is required")
    if user.email and not User.is_valid_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email address")
    if len(user.password) < 8:
        raise HTTPException(status_code=400,
                            detail="Password must be at least 8 characters")
    existing_user = db.query(User).filter(User.username == user).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    new_user = User(username=user.username, password=bcrypt.hash(user.password))
    try:
        db.add(new_user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500,
                            detail="An error occurred while creating the user") from e
    return {"message": "User created successfully"}

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user(user_id: UserBase, db: Session = Depends(get_db)):
    """Fetch a user from the users table"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
