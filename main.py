from fastapi import FASTAPI, HTTPException
import models as models
from database import engine
from sqlalchemy import Session

app = FASTAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users")
app.include_router(diaries.router, prefix="/diaries")
app.include_router(tags.router, prefix="/tags")

