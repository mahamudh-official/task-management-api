from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine
from app.exception_handlers.exception import user_exception_handler
from app.exceptions.user import UserException
from app.models.base import Base
from app.models.user import User
from app.routers.user_routers import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.add_exception_handler(UserException, user_exception_handler)

app.include_router(user_router)

@app.get("/health")
def health():
    return {"status": "ok"}