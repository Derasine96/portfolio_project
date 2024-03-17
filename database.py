from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError


URL_DATABASE = 'mysql+pymysql://root:root@localhost:3306/PersonalDiary'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get a new database session"""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        print(f"Error occurred while creating database connection: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database connection error") from e
    finally:
        db.close()
