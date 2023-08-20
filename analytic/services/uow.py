from kafka_adapter import KafkaProducer
from sqlalchemy.ext.asyncio import AsyncSession

from application.settings.broker import Settings as kafka_settings
from repositories.task.task import TaskRepo
from repositories.uow_base import KafkaProducerBaseUoW, SQLAlchemyBaseUoW
from services.task import TaskUoWInterface


class BaseUoW(
    SQLAlchemyBaseUoW,
    KafkaProducerBaseUoW,
    TaskUoWInterface,
):
    def __init__(
        self,
        session: AsyncSession,
        producer: KafkaProducer,
        kafka_app_settings: kafka_settings,
        task_repo: TaskRepo,
    ) -> None:
        self.task_repo = task_repo(session)
        SQLAlchemyBaseUoW.__init__(self, session)
        KafkaProducerBaseUoW.__init__(self, producer, kafka_app_settings)
