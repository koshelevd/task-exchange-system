from pydantic import Field, StrictInt, StrictStr

from db.tables.task import Status
from dto.base import BaseSchema, ORMBaseSchema


class TaskCreateDto(BaseSchema):
    description: StrictStr = Field(example="Task 1", description="Task description")
    status: Status = Field(example="IN_PROGRESS", description="Task status")
    employee_id: StrictInt = Field(example=1, description="Employee id")


class TaskUpdateDto(BaseSchema):
    status: Status | None = Field(example="IN_PROGRESS", description="Task status")
    employee_id: StrictInt | None = Field(example=1, description="Employee id")


class TaskResponseSchema(ORMBaseSchema):
    description: StrictStr = Field(example="Task 1", description="Task description")
    status: Status = Field(example="IN_PROGRESS", description="Task status")
    fee: StrictInt = Field(example=100, description="Task fee")
    payment: StrictInt = Field(example=100, description="Task payment")
    employee_id: StrictInt = Field(example=1, description="Employee id")


TaskMultiResponseSchema = TaskResponseSchema | list[TaskResponseSchema]
