class TaskException(Exception):

    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class TaskNotFoundException(TaskException):

    def __init__(self, task_id: int):
        super().__init__(
            message=f"Task with id '{task_id}' not found",
            status_code=404,
        )

class TaskForbiddenException(TaskException):
    def __init__(self):
        super().__init__(
            message="You do not have permission to access this resource",
            status_code=403,
        )
