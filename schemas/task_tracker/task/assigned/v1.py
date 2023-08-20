import uuid

from pydantic import BaseModel

from schemas.properties_schema import EventPropertiesSchema


class TaskAssignedEventDto(BaseModel):
    properties: EventPropertiesSchema
    task_id: uuid.UUID
    employee_id: uuid.UUID
