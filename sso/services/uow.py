from kafka_adapter import KafkaProducer
from sqlalchemy.ext.asyncio import AsyncSession

from application.settings.broker import Settings as kafka_settings
from repositories.uow_base import KafkaProducerBaseUoW, SQLAlchemyBaseUoW
from repositories.users_repository import UserRepository
from services.users.interfaces import UserUoWInterface


class BaseUoW(
    SQLAlchemyBaseUoW,
    KafkaProducerBaseUoW,
    UserUoWInterface,
):
    def __init__(
        self,
        session: AsyncSession,
        producer: KafkaProducer,
        kafka_app_settings: kafka_settings,
        user_repo: UserRepository,
    ) -> None:
        self.user_repo = user_repo(session)
        SQLAlchemyBaseUoW.__init__(self, session)
        KafkaProducerBaseUoW.__init__(self, producer, kafka_app_settings)
