import uuid
from datetime import datetime

from pydantic import BaseModel

from schemas.properties_schema import EventPropertiesSchema


class UserUpdatedEventDto(BaseModel):
    properties: EventPropertiesSchema
    public_id: uuid.UUID
    name: str | None
    role: str | None
    timestamp: datetime
