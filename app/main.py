from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.exception_handlers.task import task_exception_handler
from app.exception_handlers.user import user_exception_handler
from app.exceptions.task import TaskException
from app.exceptions.user import UserException
from app.routers.task_routers import router as task_router
from app.routers.user_routers import router as user_router

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.add_exception_handler(UserException, user_exception_handler)
app.add_exception_handler(TaskException, task_exception_handler)

app.include_router(user_router)
app.include_router(task_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/health")
def health():
    return {"status": "ok"}



