from fastapi import FastAPI
import database
from database import engine
from routes import users
from routes import diaries
from routes import tags
from routes import auth
from routes import quotes
from routes import themes

app = FastAPI()
database.Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users")
app.include_router(diaries.router, prefix="/diaries")
app.include_router(tags.router, prefix="/tags")
app.include_router(auth.router, prefix="/auth")
app.include_router(quotes.router, prefix="/quotes")
app.include_router(themes.router, prefix="/theme-options")

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()