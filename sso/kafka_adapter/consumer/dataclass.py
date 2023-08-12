from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4

Headers = list[tuple[str, bytes]]


@dataclass
class ConsumerSettings:
    bootstrap_servers: str
    group_id: str
    auto_commit_interval_ms: int = 1000
    auto_offset_reset: str = "earliest"
    check_crcs: bool = True
    consumer_timeout_ms: int = 180000
    heartbeat_interval_ms: int = 3000
    isolation_level: str = "read_committed"
    max_partition_fetch_bytes: int = 10485760
    max_poll_interval_ms: int = 300000
    metadata_max_age_ms: int = 50000
    request_timeout_ms: int = 40000
    session_timeout_ms: int = 10000


@dataclass
class ConsumerEvent:
    topic: str
    value: str | dict[str, Any]
    key: str | int | UUID = uuid4()


@dataclass
class RetryHeaders:
    original_topic: str
    current_retries: int
    max_retries_count: int
    retry_delay: int

    def serialize(self) -> Headers:
        return [
            ("x-original-topic", self.original_topic.encode()),
            ("x-current-retries", str(self.current_retries).encode()),
            ("x-max-retries-count", str(self.max_retries_count).encode()),
            ("x-retry-delay", str(self.retry_delay).encode()),
        ]
