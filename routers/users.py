from database import get_db
from models.user import UserBase, User
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.user import User, UserBase, UserResponse
from database import get_db
from passlib.hash import bcrypt

router = APIRouter()


@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    """Create a new user"""
    if not user.username:
        raise HTTPException(status_code=400, detail="Username is required")
    if not user.password:
        raise HTTPException(status_code=400, detail="Password is required")
    if user.email and not User.is_valid_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email address")
    if len(user.password) < 8:
        raise HTTPException(status_code=400,
                            detail="Password must be at least 8 characters")
    existing_username = db.query(User).filter(
        User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=409, detail="Username already exists")
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=user.username, email=user.email,
                    password=hashed_password.decode('utf-8'))
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}


@router.put("/users/{username}", response_model=UserBase)
def update_user_username(username: str, new_info: UserBase, db: Session = Depends(get_db)):
    """Update a user by their username."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if "email" in new_info.dict() and new_info.email != user.email:
        if any(existing_user.email == new_info.email
               for existing_user in db.query(User).all()):
            raise HTTPException(
                status_code=400, detail="Email already registered")
    user.copy_from(new_info)
    db.commit()
    return user


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Fetch a user from the users table"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/me/", status_code=204)
async def delete_user(user: User = Depends(get_user), db: Session = Depends(get_db)):
    """Delete the currently authenticated user account"""
    db.delete(user)
    db.commit()
