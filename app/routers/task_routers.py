from typing import Literal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    return task_service.create(task, current_user.id)

@router.get("/", response_model=TaskListResponse)
def get_tasks(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    sort_by: Literal["created_at", "due_date"] = "created_at",
    order: Literal["asc", "desc"] = "desc",
    is_completed: bool | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    return task_service.get_all_tasks(current_user.id, page, limit, sort_by, order, is_completed)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    return task_service.get_task_by_id(task_id, current_user.id
)

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    return task_service.update_task(task_id, current_user.id, task_data)

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id:int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    task_service.delete_task(task_id, current_user.id)