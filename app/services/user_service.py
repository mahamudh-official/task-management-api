from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.exceptions.user import (
    AuthenticationException,
    InActiveUserException,
    UserAlreadyExistsException,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(self.db)
        self.refresh_token_repository = RefreshTokenRepository(self.db)

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

        refresh_token = create_refresh_token({"sub": str(existing_user.id)})

        refresh_token_model = RefreshToken(
            token=refresh_token,
            user_id=existing_user.id,
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.refresh_token_expiration_days),
        )

        try:
            self.refresh_token_repository.create(refresh_token_model)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise

        return {
            "access_token": token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_access_token(self, refresh_token: str):
        payload = decode_refresh_token(refresh_token)

        stored_refresh_token = self.refresh_token_repository.get_by_token(refresh_token)

        if stored_refresh_token is None:
            raise AuthenticationException()

        if stored_refresh_token.revoked:
            raise AuthenticationException()
        
        try:
            user_id = int(payload.get("sub"))
        except (KeyError, ValueError, TypeError):
            raise AuthenticationException()

        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise AuthenticationException()

        token = create_access_token({"sub": str(user.id)})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    def logout(self, refresh_token: str)-> None:

        stored_refresh_token = self.refresh_token_repository.get_by_token(refresh_token)

        if stored_refresh_token is None:
            raise AuthenticationException()

        if stored_refresh_token.revoked:
            raise AuthenticationException()

        try:
            self.refresh_token_repository.revoke(stored_refresh_token)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise
