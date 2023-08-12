from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import User
from dto.schemas.request import CommonBaseQueryParamSchema
from services.interfaces import UoWDataBaseInterface, UoWKafkaProducerBaseInterface


class UserInterface(ABC):
    @abstractmethod
    async def is_exists(self, **kwargs) -> bool:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int, is_active: bool = True) -> User | None:
        ...

    @abstractmethod
    async def get_all_users(
        self, common_params: CommonBaseQueryParamSchema = CommonBaseQueryParamSchema(), **kwargs
    ) -> list[User]:
        ...

    @abstractmethod
    async def create_user(self, **kwargs) -> User:
        ...

    @abstractmethod
    async def update_user(self, user_id: int, **kwargs) -> None:
        ...

    @abstractmethod
    async def delete_user_by_id(self, user_id: int) -> None:
        ...


class UserUoWInterface(UoWDataBaseInterface, UoWKafkaProducerBaseInterface):
    user_repo: UserInterface
    session: AsyncSession
