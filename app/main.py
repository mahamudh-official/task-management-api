from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

@app.get("/health")
def health():
    return {"status": "ok"}