from fastapi import FastAPI
import database
from database import engine
from routers import users
from routers import diaries
from routers import tags
from routers import auth

app = FastAPI()
database.Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users")
app.include_router(diaries.router, prefix="/diaries")
app.include_router(tags.router, prefix="/tags")
app.include_router(auth.router, prefix="/auth")
