import uuid
from datetime import datetime

from pydantic import BaseModel

from schemas.properties_schema import EventPropertiesSchema


class AuditRecordCreatedEventDto(BaseModel):
    properties: EventPropertiesSchema
    account_id: uuid.UUID
    sum: float
    timestamp: datetime
    type: str
