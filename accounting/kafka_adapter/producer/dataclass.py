from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4


@dataclass
class ProducerSettings:
    acks: str | int
    bootstrap_servers: str
    transactional_id: str
    enable_idempotence = True
    linger_ms: int = 0
    max_request_size: int = 1048576


@dataclass
class ProducerEvent:
    topic: str
    value: str | dict[str, Any]
    key: str | int | UUID = uuid4()
    headers: dict[str, Any] | None = None
