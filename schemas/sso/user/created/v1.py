import uuid
from datetime import datetime

from pydantic import BaseModel

from schemas.properties_schema import EventPropertiesSchema


class UserCreatedEventDto(BaseModel):
    properties: EventPropertiesSchema
    public_id: uuid.UUID
    name: str
    role: str
    timestamp: datetime
