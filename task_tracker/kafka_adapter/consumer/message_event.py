import logging
from typing import Callable

from kafka_adapter.constants import LOGGER_PREFIX
from kafka_adapter.consumer.dataclass import Headers, RetryHeaders
from kafka_adapter.producer.dataclass import ProducerEvent
from kafka_adapter.producer.producer import KafkaProducer


class SimpleMessageEvent:
    def __init__(self, handler: Callable):
        self._logging = logging.getLogger(LOGGER_PREFIX)
        self.handler = handler

    async def handle(self, messages: list) -> None:
        for msg in messages:
            if msg:
                self._logging.info(
                    f"Consumed: {msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}, {msg.timestamp}"
                )
                try:
                    await self.handler(msg.value)
                except Exception as exc:
                    self._logging.exception(f"Unexpected error occurred: {exc}")


class DurableMessageEvent:
    def __init__(
        self, handler: Callable, retry_topic: str, retry_count: int, retry_timeout: int, producer: KafkaProducer
    ):
        self._logging = logging.getLogger(LOGGER_PREFIX)
        self.handler = handler
        self.retry_topic = retry_topic
        self.retry_count = retry_count
        self.retry_timeout = retry_timeout
        self.producer = producer

    def _get_retry_headers(self, msg) -> Headers:
        return RetryHeaders(
            original_topic=msg.topic,
            current_retries=0,
            max_retries_count=self.retry_count,
            retry_delay=self.retry_timeout,
        ).serialize()

    def _get_retry_event(self, msg) -> ProducerEvent:
        headers = self._get_retry_headers(msg)
        return ProducerEvent(
            topic=self.retry_topic,
            value=msg.value,
            key=msg.key,
            headers=headers,
        )

    async def handle(self, messages: list) -> None:
        for msg in messages:
            if msg:
                self._logging.info(
                    f"Consumed: {msg.topic}, {msg.partition}, {msg.offset}, {msg.key}, {msg.value}, {msg.timestamp}"
                )
                try:
                    await self.handler(msg.value)
                except Exception as exc:
                    self._logging.exception(
                        f"Unexpected error occurred: {exc}. Sending to retry topic: {self.retry_topic}"
                    )
                    event = self._get_retry_event(msg)
                    self._logging.error(f"RETRY EVENT: {event}")
                    # await self.producer.send(self.retry_topic, msg.value)


class MessageEventFactory:
    @classmethod
    async def create_simple_event(cls, handler: Callable) -> SimpleMessageEvent:
        return SimpleMessageEvent(handler=handler)

    @classmethod
    async def create_durable_event(
        cls, handler: Callable, retry_topic: str, retry_count: int, retry_timeout: int, producer: KafkaProducer
    ) -> DurableMessageEvent:
        return DurableMessageEvent(
            handler=handler,
            retry_topic=retry_topic,
            retry_count=retry_count,
            retry_timeout=retry_timeout,
            producer=producer,
        )
