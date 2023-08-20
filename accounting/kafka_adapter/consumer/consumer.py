import json
import logging
from dataclasses import asdict
from typing import Any, Callable
from uuid import UUID

from aiokafka import AIOKafkaConsumer, ConsumerStoppedError
from kafka_adapter.constants import LOGGER_PREFIX
from kafka_adapter.consumer.dataclass import ConsumerSettings
from kafka_adapter.consumer.message_event import MessageEventFactory
from kafka_adapter.producer.dataclass import ProducerSettings
from kafka_adapter.producer.producer import KafkaProducer


class KafkaConsumer:
    def __init__(
        self,
        consumer_settings: ConsumerSettings,
        producer_settings: ProducerSettings | None = None,
    ):
        self.consumer_settings = consumer_settings
        self.message_factory = MessageEventFactory()
        self._logging = logging.getLogger(LOGGER_PREFIX)
        self._producer = None if producer_settings is None else KafkaProducer(producer_settings)

    @staticmethod
    def key_deserializer(obj: bytes) -> UUID | str:
        if isinstance(obj, bytes):
            return obj.decode()

    @staticmethod
    def deserializer(obj: bytes) -> Any:
        return json.loads(obj.decode())

    async def _get_aiokafka_consumer(self, topics: list[str] | str) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            topics,
            **asdict(self.consumer_settings),
            enable_auto_commit=True,
            key_deserializer=self.key_deserializer,
            value_deserializer=self.deserializer,
        )

    async def _get_message(
        self, topics: list[str] | str, handler: Callable, timeout_ms: int, max_records: int | None
    ) -> None:
        # Всегда автокоммитим сообщения
        consumer = await self._get_aiokafka_consumer(topics=topics)
        await consumer.start()
        while True:
            try:
                result = await consumer.getmany(timeout_ms=timeout_ms, max_records=max_records)
                if not result:
                    continue
                for topic, messages in result.items():
                    await handler(messages=messages)
            except ConsumerStoppedError:
                continue
            except Exception as exc:
                self._logging.exception(f"Unexpected error occurred: {exc}")
            except KeyboardInterrupt:
                self._logging.info("Trying to gracefully stop kafka consumer")
                await consumer.stop()
                self._logging.info("Stopping done")

    async def register_simple_event(
        self,
        topics: list[str] | str,
        message_handler: Callable,
        timeout_ms: int = 1000,
        max_records: int | None = None,
    ) -> None:
        event_factory = await self.message_factory.create_simple_event(handler=message_handler)
        await self._get_message(
            topics=topics, handler=event_factory.handle, timeout_ms=timeout_ms, max_records=max_records
        )

    async def register_durable_event(
        self,
        topics: list[str] | str,
        message_handler: Callable,
        retry_topic: str,
        retry_count: int,
        retry_timeout: int,
        producer: KafkaProducer | None = None,
        timeout_ms: int = 1000,
        max_records: int | None = None,
    ) -> None:
        event_factory = await self.message_factory.create_durable_event(
            handler=message_handler,
            retry_topic=retry_topic,
            retry_count=retry_count,
            retry_timeout=retry_timeout,
            producer=producer or self._producer,
        )
        await self._get_message(
            topics=topics, handler=event_factory.handle, timeout_ms=timeout_ms, max_records=max_records
        )
