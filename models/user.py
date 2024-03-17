import re
from sqlalchemy import Column, Integer, String, Date
from database import Base
from pydantic import BaseModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    """Create table for user authentication"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(45), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password1 = Column(String(60), nullable=False)
    password2 = Column(String(64), nullable=False)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100))
    date_of_birth = Column(Date, nullable=False)   
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Check if the provided email address is valid."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))   
    @staticmethod
    def is_valid_password(password: str) -> bool:
        """Check if the provided password meets complexity requirements."""
        if len(password) < 8:
            return False
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[^a-zA-Z0-9]', password))
        if not (has_lowercase and has_uppercase and has_digit and has_special):
            return False
        return True    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify the provided password against the hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

class UserBase(BaseModel):
    """Validator for request from database"""
    username: str
    password:str
    email: str  
class UserLogin(BaseModel):
    """Validator for user login request"""
    username: str
    password: str
class UserSignup(BaseModel):
    """Validator for signup"""
    username: str
    password:str
    email: str
    password: str
    firstName: str
    lastName: str
    date_of_birth: str
    