from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings
from app.exceptions.user import AuthenticationException

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict):
    payload = data.copy()

    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expiration_minutes)
    payload["exp"] = exp

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("sub") is None:
            raise AuthenticationException()
        return payload

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        print(type(e).__name__, str(e))
        raise AuthenticationException()
    