from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from controllers.routers.v1.user.dependencies import get_user_service
from controllers.stub import Stub
from dto.users_schemas import TokenSchema, UserDTO, UserResponseEntity
from services import UserService

router = APIRouter()


@router.post(
    "/auth",
    response_model=TokenSchema,
    summary="Create access and refresh tokens for user",
)
async def login(data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(Stub(UserService))):
    """Create access and refresh tokens for user."""
    return await service.signin(data.username, data.password)


@router.post(
    "/register",
    response_model=UserResponseEntity,
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(data: UserDTO, service: UserService = Depends(Stub(UserService))):
    """Register new user."""
    user = await service.signup(data.email, data.password)
    return user
