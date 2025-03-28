import logging
import sys
from enum import Enum
from uuid import uuid4


class Logger:
    class LoggingLevelEnum(int, Enum):
        DEBUG = logging.DEBUG
        INFO = logging.INFO
        WARNING = logging.WARNING
        ERROR = logging.ERROR
        CRITICAL = logging.CRITICAL

    def __init__(
        self,
        process_id: str | None = None,
        level: int = LoggingLevelEnum.INFO.value,
        force: bool = True,
    ):
        self._process_id: str = process_id or str(uuid4())
        self._level: int = level
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=level,
            force=force,
        )
        self._logger: logging.Logger = logging.getLogger()
        self._logger.propagate = True

        self._logger.handlers.clear()
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
        stderr_handler = logging.StreamHandler()
        stderr_handler.setLevel(logging.WARNING)
        self._logger.addHandler(stdout_handler)
        self._logger.addHandler(stderr_handler)

    @property
    def process_id(self) -> str:
        return self._process_id

    @process_id.setter
    def process_id(self, process_id):
        self._process_id = process_id

    @property
    def level(self) -> int:
        return self._level

    def log_debug(self, msg):
        self._logger.debug(f"{self._process_id}: {msg}")

    def log_info(self, msg):
        self._logger.info(f"{self._process_id}: {msg}")

    def log_warning(self, msg):
        self._logger.warning(f"{self._process_id}: {msg}")

    def log_error(self, msg):
        self._logger.error(f"{self._process_id}: {msg}")

    def log_critical(self, msg):
        self._logger.critical(f"{self._process_id}: {msg}")
