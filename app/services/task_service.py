import math

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.exceptions.task import InvalidTaskPageException, TaskForbiddenException, TaskNotFoundException
from app.exceptions.user import AuthenticationException
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskListResponse, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository= TaskRepository(self.db)

    def create(self, task: TaskCreate, user_id: int)-> Task:
        task_model = Task(
            title= task.title,
            description= task.description,
            due_date= task.due_date,
            user_id=user_id
        )

        try:
            self.task_repository.create(task_model)
            self.db.commit()
            self.db.refresh(task_model)
            return task_model
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_all_tasks(
        self,
        user_id: int,
        page: int = 1,
        limit: int = 10,
        sort_by: str = "created_at",
        order: str = "desc",
        is_completed: bool | None = None
    ) -> TaskListResponse:
        skip = (page - 1) * limit

        total_tasks = self.task_repository.count_by_user_id(user_id, is_completed)

        total_pages = math.ceil(total_tasks / limit)

        if total_pages > 0 and page > total_pages:
            raise InvalidTaskPageException(page)

        tasks = self.task_repository.get_all_by_user_id(
            user_id, skip, limit, sort_by, order, is_completed
        )

        return TaskListResponse(
            items=tasks,
            total=total_tasks,
            page=page,
            limit=limit,
            total_pages=total_pages,
        )

    def get_task_by_id(self, task_id: int, user_id: int) -> Task | None:
        task = self.task_repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundException(task_id)

        if task.user_id != user_id:
            raise TaskForbiddenException()

        return task

    def update_task(self, task_id: int, user_id: int, task_data: TaskUpdate)-> Task:
        task = self.task_repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundException(task_id)

        if task.user_id != user_id:
            raise TaskForbiddenException()

        update_data = task_data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(task, key, value)

        try:
            self.task_repository.update(task)
            self.db.commit()
            self.db.refresh(task)
            return task
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundException(task_id)

        if task.user_id != user_id:
            raise TaskForbiddenException()

        try:
            self.task_repository.delete(task)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise        
