from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.task import TaskException


async def task_exception_handler(
    request: Request,
    excep: TaskException,
):
    return JSONResponse(
        status_code=excep.status_code,
        content={"message": excep.message},
    )