from typing import Any, Sequence

from sqlalchemy import Row, RowMapping, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from db.tables import Task
from dto.schemas.request import CommonBaseQueryParamSchema
from repositories.const import SortingType
from repositories.repo_base import BaseRepository
from services.task import TaskInterface


class TaskRepo(BaseRepository, TaskInterface):
    async def is_exists(self, **kwargs) -> bool:
        query = select(select(Task.id).filter_by(**kwargs).exists())
        result = await self.session.execute(query)
        return result.scalar()

    async def get_task_by_id(self, task_id: int, is_active: bool = True) -> Task | None:
        query = select(Task).options(joinedload(Task.employee)).filter_by(id=task_id, is_active=is_active)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_tasks(
        self, common_params: CommonBaseQueryParamSchema = CommonBaseQueryParamSchema(), **kwargs
    ) -> list[Task] | Sequence[Row | RowMapping | Any]:
        query = (
            select(Task)
            .options(joinedload(Task.employee))
            .filter_by(is_active=common_params.is_active, **kwargs)
            .limit(common_params.limit)
            .offset(common_params.offset)
        )
        if common_params.order_by:
            query = query.order_by(getattr(SortingType, common_params.ordering)(common_params.order_by))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_task(self, **kwargs) -> Task:
        task = Task(**kwargs)
        unique_fields_exceptions = await self.validate_uniques(task)
        if unique_fields_exceptions:
            raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)
        self.session.add(task)
        await self.session.flush([task])
        return task

    async def update_task(self, task_id: int, **kwargs) -> None:
        unique_fields_exceptions = await self.validate_uniques_by_values(Task, kwargs)
        if unique_fields_exceptions:
            raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)
        query = update(Task).values(**kwargs).filter_by(id=task_id)
        await self.session.execute(query)

    async def delete_task_by_id(self, task_id: int) -> None:
        query = update(Task).filter_by(id=task_id).values(is_active=False)
        await self.session.execute(query)
