from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task)-> Task:
        self.db.add(task)
        return task

    def get_by_id(self, task_id: int)-> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_by_user_id(self, user_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.user_id == user_id).all()

    def update(self, task: Task) -> Task:
        self.db.add(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)