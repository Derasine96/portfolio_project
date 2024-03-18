from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from jose import jwt
from models.user import User, UserLogin, UserSignup
from database import get_db
import bcrypt
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "alx123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def sign_up(user_signup: UserSignup, db: Session = Depends(get_db)):
    """Sign up a new user"""
    hashed_password = bcrypt.hashpw(
        user_signup.password1.encode('utf-8'), bcrypt.gensalt())
    new_user = User(
        username=user_signup.username,
        email=user_signup.email,
        password=hashed_password.decode('utf-8'),
        firstName=user_signup.firstName,
        lastName=user_signup.lastName,
        date_of_birth=user_signup.date_of_birth
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as e:
        print(f"Error occurred while adding user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error occurred") from e
    return new_user


@router.post("/login", response_model=str)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user based on username and password"""
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    if not pwd_context.verify(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_payload = {
        "sub": user.username,
        "exp": datetime.utcnow() + access_token_expires
    }
    access_token = jwt.encode(access_token_payload,
                              SECRET_KEY, algorithm=ALGORITHM)
    return access_token
