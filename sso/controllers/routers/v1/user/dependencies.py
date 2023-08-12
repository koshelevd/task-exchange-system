from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from starlette import status

from application.settings.app import Settings as app_settings
from controllers.dependencies import get_event_constructor, get_uow
from db.tables import User
from dto.users_schemas import TokenPayload
from services import UserService
from services.errors import NotAuthenticatedError, ObjectNotFoundError
from services.event_constructor import EventConstructor
from services.uow import BaseUoW

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth",
    scheme_name="JWT",
    auto_error=False,
)


def get_user_service(
    uow: BaseUoW = Depends(get_uow), event_constructor: EventConstructor = Depends(get_event_constructor)
) -> UserService:
    return UserService(uow=uow, event_constructor=event_constructor)


async def get_current_user(
    token: str = Depends(reuseable_oauth),
    uow: BaseUoW = Depends(get_uow),
) -> User | None:
    if token is None:
        raise NotAuthenticatedError("User")
    try:
        payload = jwt.decode(
            token,
            app_settings.JWT_SECRET_KEY,
            algorithms=[app_settings.ALGORITHM],
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await uow.user_repo.get_user_by_email(token_data.sub)
    if user is None:
        raise ObjectNotFoundError("User")
    return user
