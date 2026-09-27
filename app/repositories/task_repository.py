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

    def get_all_by_user_id(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 10,
        sort_by: str = "created_at",
        order: str = "desc",
        is_completed: bool | None = None
    ) -> list[Task]:

        query = self.db.query(Task).filter(Task.user_id == user_id)

        if is_completed is not None:
            query = query.filter(Task.is_completed == is_completed)

        if sort_by == "created_at":
            column = Task.created_at
        else:
            column = Task.due_date

        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

        return (
            query
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, task: Task) -> Task:
        self.db.add(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)

    def count_by_user_id(self, user_id: int, is_completed: bool | None = None) -> int:
        query = self.db.query(Task).filter(Task.user_id == user_id)
        if is_completed is not None:
            query = query.filter(Task.is_completed == is_completed)
        return query.count()
