import inspect
import logging


class BaseLogger:
    """
    Base logging class.
    Returns the registrar with the composite name name.
    Name is defined as the ClassName.MethodName where the base class method
    was called. Delegates the log call to the underlying logger.
    The level is determined by the base logger flag, _log() is called directly.
    """

    def debug(self, msg, *args, **kwargs):
        self.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log(logging.ERROR, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        kwargs["exc_info"] = 1
        self.log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log(logging.CRITICAL, msg, *args, **kwargs)

    @staticmethod
    def log(level, msg, *args, **kwargs):
        log_from_class = inspect.stack()[2][0].f_locals.get("self").__class__.__name__
        log_from_method = inspect.stack()[2][3]
        logger = logging.getLogger(f"{log_from_class}.{log_from_method}")
        logger._log(level, msg, args, **kwargs)  # noqa


logg = BaseLogger()
