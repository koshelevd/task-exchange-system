from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import Task
from dto.schemas.request import CommonBaseQueryParamSchema
from services.interfaces import UoWDataBaseInterface, UoWKafkaProducerBaseInterface


class TaskInterface(ABC):
    @abstractmethod
    async def is_exists(self, **kwargs) -> bool:
        ...

    @abstractmethod
    async def get_task_by_id(self, task_id: int, is_active: bool = True) -> Task | None:
        ...

    @abstractmethod
    async def get_all_tasks(
        self, common_params: CommonBaseQueryParamSchema = CommonBaseQueryParamSchema(), **kwargs
    ) -> list[Task]:
        ...

    @abstractmethod
    async def create_task(self, **kwargs) -> Task:
        ...

    @abstractmethod
    async def update_task(self, task_id: int, **kwargs) -> None:
        ...

    @abstractmethod
    async def delete_task_by_id(self, task_id: int) -> None:
        ...


class TaskUoWInterface(UoWDataBaseInterface, UoWKafkaProducerBaseInterface):
    task_repo: TaskInterface
    session: AsyncSession
