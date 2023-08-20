import uuid

from pydantic import BaseModel

from schemas.properties_schema import EventPropertiesSchema


class AccountUpdatedEventDto(BaseModel):
    properties: EventPropertiesSchema
    employee_id: uuid.UUID
    account_id: uuid.UUID
    sum: float
    type: str
