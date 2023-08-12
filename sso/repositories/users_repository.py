from typing import Any, Sequence

from sqlalchemy import Row, RowMapping, select, update
from sqlalchemy.exc import IntegrityError

from db.tables import User
from repositories.repo_base import BaseRepository
from services.users.interfaces import UserInterface


class UserRepository(BaseRepository, UserInterface):
    """User repository"""

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Get user by email.

        :param email: users email
        :return: user
        """

        query = select(User).filter_by(email=email)
        expr = await self.session.execute(query)
        return expr.scalar_one_or_none()

    async def is_exists(self, **kwargs) -> bool:
        query = select(select(User.id).filter_by(**kwargs).exists())
        result = await self.session.execute(query)
        return result.scalar()

    async def get_user_by_id(self, user_id: int, is_active: bool = True) -> User | None:
        query = select(User).filter_by(id=user_id, is_active=is_active)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_users(self, **kwargs) -> list[User] | Sequence[Row | RowMapping | Any]:
        query = select(User).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_user(self, **kwargs) -> User:
        user = User(**kwargs)
        unique_fields_exceptions = await self.validate_uniques(user)
        if unique_fields_exceptions:
            raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)
        self.session.add(user)
        await self.session.flush([user])
        return user

    async def update_user(self, user_id: int, **kwargs) -> None:
        unique_fields_exceptions = await self.validate_uniques_by_values(User, kwargs)
        if unique_fields_exceptions:
            raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)
        query = update(User).values(**kwargs).filter_by(id=user_id)
        await self.session.execute(query)

    async def delete_user_by_id(self, user_id: int) -> None:
        query = update(User).filter_by(id=user_id).values(is_active=False)
        await self.session.execute(query)
