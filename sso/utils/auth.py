from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from application.settings.app import app_settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    print(type(password))
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_token(subject: Union[str, Any], expires_delta: int = None, refresh: bool = False) -> str:
    if refresh:
        token_lifetime = app_settings.REFRESH_TOKEN_EXPIRE_MINUTES
        secret_key = app_settings.JWT_REFRESH_SECRET_KEY
    else:
        token_lifetime = app_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        secret_key = app_settings.JWT_SECRET_KEY
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=token_lifetime)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, app_settings.ALGORITHM)
    return encoded_jwt


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return create_token(subject, expires_delta)


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return create_token(subject, expires_delta, refresh=True)
