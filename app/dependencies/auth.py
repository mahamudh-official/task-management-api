from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.exceptions.user import AuthenticationException
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    user_id = int(payload["sub"])

    repository = UserRepository(db)
    user = repository.get_by_id(user_id)
    if user is None:
        raise AuthenticationException()
    return user