from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.user import UserException


async def user_exception_handler(request: Request, excep: UserException):
    return JSONResponse(
        status_code=excep.status_code,
        content={"message": excep.message},
    )
