from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.exceptions.user import (
    AuthenticationException,
    InActiveUserException,
    UserAlreadyExistsException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(self.db)

    def create(self, user: UserCreate) -> User:
        existing_user = self.user_repository.get_by_email(user.email)

        if existing_user is not None:
            raise UserAlreadyExistsException("email",user.email)

        existing_user = self.user_repository.get_by_username(user.username)

        if existing_user is not None:
            raise UserAlreadyExistsException("username", user.username)

        existing_user = self.user_repository.get_by_phone_number(user.phone_number)
        if existing_user is not None:
            raise UserAlreadyExistsException('phone number', user.phone_number)

        user_model = User(
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            password_hash= hash_password(user.password)
        )

        try:
            self.user_repository.create(user_model)
            self.db.commit()
            self.db.refresh(user_model)
            return user_model
        except SQLAlchemyError:
            self.db.rollback()
            raise 

    def login(self, user: UserLogin):
        existing_user = self.user_repository.get_by_email(user.email)

        if existing_user is None:
            raise AuthenticationException()

        if not existing_user.is_active:
            raise InActiveUserException()

        if not verify_password(user.password, existing_user.password_hash):
            raise AuthenticationException()

        token = create_access_token({"sub": str(existing_user.id)})

        return {
            "access_token": token,
            "token_type": "bearer"
        }