from database import get_db
from models.user import UserBase, User, UserResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/users/{user_name}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user_name: str, db: Session = Depends(get_db)):
    """Fetch a user from the users table"""
    user = db.query(User).filter(User.username == user_name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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
    db.commit()
    return user


@router.delete("/users/me/", response_model=dict)
async def delete_user(user: User = Depends(get_user), db: Session = Depends(get_db)):
    """Delete the currently authenticated user account"""
    db.delete(user)
    db.commit()
    return {"message": "User successfully deleted"}
