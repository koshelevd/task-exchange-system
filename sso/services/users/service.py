from copy import copy

from email_validator import EmailSyntaxError
from pydantic import validate_email
from sqlalchemy.exc import IntegrityError
from utils.auth import create_access_token, get_hashed_password, verify_password

from db.tables import User
from dto.users_schemas import TokenSchema
from services.errors import BadRequestError, ObjectAlreadyExistsError
from services.interfaces import EventConstructorInterface
from services.users.interfaces import UserUoWInterface


class UserService:
    def __init__(self, uow: UserUoWInterface, event_constructor: EventConstructorInterface):
        self.uow = uow
        self.event_constructor = event_constructor

    async def signup(self, email: str, password: str) -> User:
        """
        Create new user.

        :param email: email
        :param password: password
        :return: user
        """
        try:
            validate_email(email)
        except EmailSyntaxError as e:
            raise BadRequestError(message=str(e))
        user = await self.uow.user_repo.get_user_by_email(email)
        if user:
            raise BadRequestError("User with this email already exist")
        hash_ = get_hashed_password(password)
        user = await self.uow.user_repo.create_user(email=email, password=hash_, role_id=1)
        self.uow.session.add(user)
        await self.uow.session.commit()
        event = self.event_constructor.create_producer_event(
            topic="user_created",
            value=user.dict(),
            key=user.id,
        )
        await self.uow.producer.send_and_wait(event)
        return user

    async def signin(self, email: str, password: str) -> TokenSchema:
        """
        Sign in user.

        :param email: email
        :param password: password
        :return: user
        """
        user = await self.uow.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            raise BadRequestError("Wrong email or password")

        access_token = create_access_token(user.email)
        refresh_token = create_access_token(user.email)
        result = TokenSchema(access_token=access_token, refresh_token=refresh_token)
        return result

    async def get_user_status(self, user: User):
        """
        Get user status.

        :param user: user
        :return: user status
        """
        ...
