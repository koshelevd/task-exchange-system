import uuid

from sqlalchemy.exc import IntegrityError

from services.errors import ObjectAlreadyExistsError
from services.interfaces import EventConstructorInterface
from services.account import AccountNotFoundError, AccountUoWInterface

from schemas.accounting.account.created.v1 import AccountCreatedEventDto
from schemas.accounting.account.updated.v1 import AccountUpdatedEventDto


class AccountService:
    def __init__(self, uow: AccountUoWInterface, event_constructor: EventConstructorInterface):
        self.uow = uow
        self.event_constructor = event_constructor

    async def create_account(self, account_data: AccountCreateDto) -> None:
        try:
            account = await self.uow.account_repo.create_account(**account_data.dict(exclude_none=True))
        except IntegrityError as exc:
            raise ObjectAlreadyExistsError(exc.params)
        else:
            await self.uow.commit()
            event = self.event_constructor.create_producer_event(
                topic=broker_settings.ACCOUNT_TOPIC, value=AccountCreatedEventDto(**account.dict()).dict()
            )
            await self.uow.send(event)

    async def update_account(self, account_id: uuid, account_data: AccountUpdateDto) -> None:
        account = await self.uow.account_repo.get_account_by_id(account_id)
        if not account:
            raise AccountNotFoundError(["account_id"], context_message=f"Account {account_id=} not found")
        try:
            await self.uow.account_repo.update_account(account_id, **account_data.dict(exclude_none=True))
        except IntegrityError as exc:
            raise ObjectAlreadyExistsError(exc.params)
        else:
            await self.uow.session.commit()
            event = self.event_constructor.create_producer_event(
                topic=broker_settings.ACCOUNT_TOPIC, value=AccountUpdatedEventDto(**account.dict()).dict()
            )
            await self.uow.send(event)
