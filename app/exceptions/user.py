class UserException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class UserNotFoundException(UserException):
    def __init__(self, email: str):
        super().__init__(message=f"User with email {email} not found", status_code=404)

class UserAlreadyExistsException(UserException):
    def __init__(self, field: str, value: str):
        super().__init__(message=f"User with {field} '{value}' already exists", status_code=409)

class AuthenticationException(UserException):
    def __init__(self):
        super().__init__(message="Credentials are invalid", status_code=401)

class InActiveUserException(UserException):
    def __init__(self):
        super().__init__(message="User is inactive", status_code=403)