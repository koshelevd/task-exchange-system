from fastapi import Depends

from controllers.dependencies import get_event_constructor, get_uow
from services import TaskService
from services.event_constructor import EventConstructor
from services.uow import BaseUoW


def get_task_service(
    uow: BaseUoW = Depends(get_uow), event_constructor: EventConstructor = Depends(get_event_constructor)
) -> TaskService:
    return TaskService(uow=uow, event_constructor=event_constructor)
