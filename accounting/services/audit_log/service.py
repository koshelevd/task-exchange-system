from sqlalchemy.exc import IntegrityError

from services.errors import ObjectAlreadyExistsError
from services.interfaces import EventConstructorInterface
from services.audit_log import AuditLogUoWInterface
from sqlalchemy.exc import IntegrityError

from schemas.accounting.audit_log.created.v1 import AuditRecordCreatedEventDto


class AuditLogService:
    def __init__(self, uow: AuditLogUoWInterface, event_constructor: EventConstructorInterface):
        self.uow = uow
        self.event_constructor = event_constructor

    async def create_audit_record(self, record_data: AuditRecordCreateDto) -> None:
        try:
            record = await self.uow.audit_record_repo.create_record(**record_data.dict(exclude_none=True))
        except IntegrityError as exc:
            raise ObjectAlreadyExistsError(exc.params)
        else:
            await self.uow.commit()
            event = self.event_constructor.create_producer_event(
                topic=broker_settings.AUDIT_TOPIC, value=AuditRecordCreatedEventDto(**record.dict()).dict()
            )
            await self.uow.send(event)
