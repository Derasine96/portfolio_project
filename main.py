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

@app.get("/")
def index():
    return {"status": "uvicorn server is working"}


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", reload=True, port=8000)

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
