import json
import logging
from dataclasses import asdict
from datetime import datetime, time, timezone
from enum import Enum, IntEnum
from typing import Any
from uuid import UUID

from aiokafka import AIOKafkaProducer
from kafka_adapter.constants import LOGGER_PREFIX
from kafka_adapter.producer.dataclass import ProducerEvent, ProducerSettings


class KafkaProducer:
    def __init__(self, producer_settings: ProducerSettings):
        self.producer_settings = producer_settings
        self._logging = logging.getLogger(LOGGER_PREFIX)

    def _serialize_value(self, obj: Any):
        """Эта функция рекурсивно преобразовывает объекты в вид, готовый для к сериализации"""
        if isinstance(obj, (datetime, time)):
            return obj.replace(tzinfo=timezone.utc).isoformat()
        if isinstance(obj, (Enum, IntEnum)):
            return obj.value
        if isinstance(obj, UUID):
            return obj.hex
        if isinstance(obj, list):
            return [self._serialize_value(x) for x in obj]
        if isinstance(obj, dict):
            return {key: self._serialize_value(value) for key, value in obj.items()}
        return obj

    def serializer(self, obj: Any) -> bytes:
        return json.dumps(self._serialize_value(obj=obj)).encode()

    async def start(self, producer_event: ProducerEvent) -> None:
        producer = AIOKafkaProducer(
            **asdict(self.producer_settings), value_serializer=self.serializer, key_serializer=self.serializer
        )
        await producer.start()

        try:
            async with producer.transaction():
                message = asdict(producer_event)
                await producer.send_and_wait(**message)
                self._logging.info(f"The message {message} was added to the kafka topic {producer_event.topic}")

        except Exception as exc:
            self._logging.exception(f"Unexpected error occurred: {exc}")

        finally:
            self._logging.info("Trying to gracefully stop kafka producer")
            await producer.stop()
            self._logging.info("Stopping done")
