from logging import (
    INFO,
    Logger,
    FileHandler,
    StreamHandler,
    Formatter,
    DEBUG,
    NOTSET,
    WARN,
    WARNING,
    ERROR,
)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class LoggerManager:

    logger = {}

    @classmethod
    def get_logger(cls, name: str = "default", level=INFO, format=LOG_FORMAT):

        key = (name, level)

        def gen_logger():
            formatter = Formatter(format)
            handler = StreamHandler()
            handler.setFormatter(formatter)
            handler.setLevel(level)
            logger = Logger(name)
            logger.addHandler(handler)
            logger.setLevel(level)
            cls.logger[key] = logger
            return logger

        return cls.logger.get(key) or gen_logger()


get_logger = LoggerManager().get_logger
