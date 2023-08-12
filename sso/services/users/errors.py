from services.errors import ObjectNotFoundError


class AddressTypeNotFoundError(ObjectNotFoundError):
    message = "Тип адреса не найден"
