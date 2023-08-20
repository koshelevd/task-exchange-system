from db.tables import Task
from dto.schemas.request import CommonBaseQueryParamSchema
from dto.task.task import TaskCreateDto, TaskUpdateDto
from services.errors import ObjectAlreadyExistsError
from services.interfaces import EventConstructorInterface
from services.task import TaskNotFoundError, TaskUoWInterface
from sqlalchemy.exc import IntegrityError

from schemas.task_tracker.task.assigned.v1 import TaskAssignedEventDto
from schemas.task_tracker.task.completed.v1 import TaskCompletedEventDto
from schemas.task_tracker.task.created.v1 import TaskCreatedEventDto


class TaskService:
    def __init__(self, uow: TaskUoWInterface, event_constructor: EventConstructorInterface):
        self.uow = uow
        self.event_constructor = event_constructor

    async def get_tasks(
        self,
        common_params: CommonBaseQueryParamSchema,
        task_id: int | None = None,
    ) -> list[Task] | Task:
        if task_id:
            result = await self.uow.task_repo.get_task_by_id(task_id, common_params.is_active)
            if not result:
                raise TaskNotFoundError(["task_id"], context_message=f"Task {task_id=} not found")
        else:
            result = await self.uow.task_repo.get_all_tasks(common_params)
        return result

    async def create_task(self, task_data: TaskCreateDto) -> None:
        try:
            task = await self.uow.task_repo.create_task(**task_data.dict(exclude_none=True))
        except IntegrityError as exc:
            raise ObjectAlreadyExistsError(exc.params)
        else:
            await self.uow.commit()
            event = self.event_constructor.create_producer_event(
                topic=broker_settings.TASK_TOPIC, value=TaskCreatedEventDto(**task.dict()).dict()
            )
            await self.uow.send(event)

    async def update_task(self, task_id: int, task_data: TaskUpdateDto) -> None:
        task = await self.uow.task_repo.get_task_by_id(task_id)
        if not task:
            raise TaskNotFoundError(["task_id"], context_message=f"Task {task_id=} not found")
        try:
            await self.uow.task_repo.update_task(task_id, **task_data.dict(exclude_none=True))
        except IntegrityError as exc:
            raise ObjectAlreadyExistsError(exc.params)
        else:
            await self.uow.session.commit()
            if task_data.is_assigned:
                event = self.event_constructor.create_producer_event(
                    topic=broker_settings.TASK_TOPIC, value=TaskAssignedEventDto(**task.dict()).dict()
                )
            else:
                event = self.event_constructor.create_producer_event(
                    topic=broker_settings.TASK_TOPIC, value=TaskCompletedEventDto(**task.dict()).dict()
                )
            await self.uow.send(event)
