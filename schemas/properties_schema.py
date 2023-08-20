from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class EventVersion(Enum):
    v1 = 1


class EventPropertiesSchema(BaseModel):
    event_id: str
    event_version: EventVersion = EventVersion.v1
    event_name: str
    event_time: datetime
    producer: str
