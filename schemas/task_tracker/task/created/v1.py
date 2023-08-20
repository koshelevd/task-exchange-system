import uuid

from pydantic import BaseModel

from schemas.properties_schema import EventPropertiesSchema
from task_tracker.task.task_status import TaskStatus


class TaskCreatedEventDto(BaseModel):
    properties: EventPropertiesSchema
    task_id: uuid.UUID
    description: str
    status: TaskStatus
    fee: float
    payment: float
