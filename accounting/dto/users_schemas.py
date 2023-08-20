from dto.base import BaseSchema, ORMBaseSchema


class BaseUserSchema(BaseSchema):
    email: str


class UserDTO(BaseUserSchema):
    password: str


class UserResponseEntity(ORMBaseSchema):
    id: int
    email: str


class TokenSchema(BaseSchema):
    access_token: str
    refresh_token: str


class TokenPayload(BaseSchema):
    sub: str = None
    exp: int = None
