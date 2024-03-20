from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from models.user import User, UserLogin, UserSignup
from database import get_db
from sqlalchemy.exc import SQLAlchemyError
from utils.pass_hash import hash_password, verify_password


router = APIRouter()


@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def sign_up(user_signup: UserSignup, db: Session = Depends(get_db)):
    """Sign up a new user"""
    if not user_signup.username:
        raise HTTPException(status_code=400, detail="Username is required")
    if not user_signup.password:
        raise HTTPException(status_code=400, detail="Password is required")
    if not User.is_valid_password(user_signup.password):
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters and contain at least one lowercase letter, one uppercase letter, one digit, and one special character")
    if user_signup.email and not User.is_valid_email(user_signup.email):
        raise HTTPException(status_code=400, detail="Invalid email address")
    existing_username = db.query(User).filter(
        User.username == user_signup.username).first()
    if existing_username:
        raise HTTPException(status_code=409, detail="Username already exists")
    existing_email = db.query(User).filter(
        User.email == user_signup.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = User.hash_password(user_signup.password)
    new_user = User(username=user_signup.username,
                    email=user_signup.email, password=hashed_password, firstName=user_signup.firstName, lastName=user_signup.lastName, date_of_birth=user_signup.date_of_birth)
    db.add(new_user)
    db.commit()
    return new_user.to_dict()


SECRET_KEY = "alx123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/login", response_model=str)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user based on username and password"""
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email address")
    if not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_payload = {
        "sub": user.email, "exp": datetime.utcnow() + access_token_expires
    }
    access_token = jwt.encode(access_token_payload,
                              SECRET_KEY, algorithm=ALGORITHM)
    return access_token


@router.post("/logout")
async def logout(token: Optional[str] = Depends(oauth2_scheme)):
    """Invalidate a token (logout)
    This endpoint invalidates the provided token, effectively logging out the user.
    If no token is provided, the user will not be logged out and a 401 Unauthorized response will be returned.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not provided")
    return {"detail": "Successfully logged out"}
