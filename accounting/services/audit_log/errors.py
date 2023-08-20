from services.errors import ObjectNotFoundError


class TaskNotFoundError(ObjectNotFoundError):
    message = "Task not found"
