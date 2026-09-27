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

def create_access_token(data: dict,):
    payload = data.copy()

    now = datetime.now(timezone.utc)

    exp = now + timedelta(minutes=settings.access_token_expiration_minutes)
    payload["iat"]= now
    payload["type"]= "access"
    payload["exp"] = exp

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def create_refresh_token(data: dict):
    payload = data.copy()

    now = datetime.now(timezone.utc)

    exp = now + timedelta(days=settings.refresh_token_expiration_days)
    payload["iat"]= now
    payload["type"]= "refresh"
    payload["exp"] = exp

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        if payload.get("type") != "access":
            raise AuthenticationException()
        
        if payload.get("sub") is None:
            raise AuthenticationException()
        return payload

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise AuthenticationException()

def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        if payload.get("type") != "refresh":
            raise AuthenticationException()
        
        if payload.get("sub") is None:
            raise AuthenticationException()
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise AuthenticationException()