import logging
import logging.handlers as handlers
from abc import abstractmethod
from typing import Any

_ERASE_LINE = '\u001b[2K'
_WHITE = "\u001b[37m"
_RED = "\u001b[31m"
_GREEN = "\u001b[32m"
_YELLOW = "\u001b[33m"
_RESET = "\u001b[0m"
_BOLD = "\u001b[1m"
_REVERSE = "\u001b[7m"


class Logger(object):

    @abstractmethod
    def progress(self, message): pass

    @abstractmethod
    def debug(self, message): pass

    @abstractmethod
    def info(self, message): pass

    @abstractmethod
    def warn(self, message): pass

    @abstractmethod
    def error(self, message): pass

    @abstractmethod
    def success(self, message): pass

    @abstractmethod
    def failure(self, message): pass

    @abstractmethod
    def command_info(self, command): pass

    @abstractmethod
    def command_output(self, output): pass


class ConsoleLogger(Logger):
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger("console")
        self.logger.handlers.clear()
        stream_handler = logging.StreamHandler()
        stream_handler.terminator = ""
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(level)

    def progress(self, message):
        if self.logger.level == logging.DEBUG:
            term = "\n"
            style = _WHITE
        else:
            style = _REVERSE
            term = "\r"

        self.logger.info(msg="{}- {}{}{}{}".format(_ERASE_LINE, style, message, _RESET, term))

    def debug(self, message):
        self.logger.debug("{}- {}{}\n".format(_ERASE_LINE, message, _RESET))

    def info(self, message):
        self.logger.info("{}- {}{}{}{}\n".format(_ERASE_LINE, _BOLD, _WHITE, message, _RESET))

    def warn(self, message):
        self.logger.warning("{}- {}{}{}\n".format(_ERASE_LINE, _YELLOW, message, _RESET))

    def error(self, message):
        self.logger.error("{}- {}{}{}\n".format(_ERASE_LINE, _RED, message, _RESET))

    def success(self, message):
        self.logger.info("{}- {}{}{}{}{}\n".format(_ERASE_LINE, _REVERSE, _BOLD, _GREEN, message, _RESET))

    def failure(self, message):
        self.logger.error("{}- {}{}{}{}\n".format(_ERASE_LINE, _REVERSE, _RED, message, _RESET))

    def command_info(self, command):
        self.logger.info(
            msg="\t ~ {}{}{}{}\n"
                .format(_REVERSE, _YELLOW, command, _RESET))

    def command_output(self, output):
        self.logger.info(output.strip())


class FileLogger(Logger):

    def __init__(self, filename, level=logging.INFO):
        file_handler = handlers.RotatingFileHandler(filename=filename, mode="a", maxBytes=1024 * 1000, backupCount=3)
        file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))

        self.logger = logging.getLogger("file")
        self.logger.setLevel(level)
        self.logger.addHandler(file_handler)

    def progress(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message, exc_info=self._exc_info(message))

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message, exc_info=self._exc_info(message))

    def error(self, message):
        self.logger.error(message, exc_info=self._exc_info(message))

    def success(self, message):
        self.logger.info(message)

    def failure(self, message):
        self.logger.error(message, exc_info=self._exc_info(message))

    def command_info(self, command):
        self.info("[Command]: {}".format(command))

    def command_output(self, output):
        self.logger.info(output.strip())

    @staticmethod
    def _exc_info(message):
        return isinstance(message, BaseException)


class NoopLogger(Logger):
    def __getattribute__(self, name: str) -> Any:
        return lambda *args, **kwrgs: None


class CompositeLogger(Logger):
    def __init__(self, *loggers: Logger):
        self.loggers = loggers

    def progress(self, message):
        self._all("progress", message)

    def debug(self, message):
        self._all("debug", message)

    def info(self, message):
        self._all("info", message)

    def warn(self, message):
        self._all("warn", message)

    def error(self, message):
        self._all("error", message)

    def success(self, message):
        self._all("success", message)

    def failure(self, message):
        self._all("failure", message)

    def command_info(self, command):
        self._all("command_info", command)

    def command_output(self, output):
        self._all("command_output", output)

    def _all(self, fn_name, *args, **kwargs):
        for logger in self.loggers:
            fn = getattr(logger, fn_name)
            fn(*args, **kwargs)


NOOP_LOGGER = NoopLogger()
