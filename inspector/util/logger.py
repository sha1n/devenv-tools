import logging
import logging.handlers as handlers
from abc import abstractmethod

_ERASE_LINE = '\x1b[2K'


class Logger(object):

    @abstractmethod
    def log(self, message): pass

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


class ConsoleLogger(Logger):

    def log(self, message):
        print("\033[1;37;40mINFO\033[0;0m: {}".format(message), end="\r")

    def debug(self, message):
        print("{}\033[0;37;40mDEBG\033[0;0m: {}\033[0;0m".format(_ERASE_LINE, message))

    def info(self, message):
        print("{}\033[1;37;40mINFO\033[0;0m: {}".format(_ERASE_LINE, message))

    def warn(self, message):
        print("{}\033[1;33;40mWARN\033[0;0m: {}".format(_ERASE_LINE, message))

    def error(self, message):
        print("{}\033[1;31;40mERRO\033[0;0m: {}".format(_ERASE_LINE, message))

    def success(self, message):
        print("{}\033[1;37;40mINFO\033[0;0m: \033[0;30;42m{}\033[0;0m".format(_ERASE_LINE, message))

    def failure(self, message):
        print("{}\033[1;31;40mERRO\033[0;0m: \033[0;37;41m{}\033[0;0m".format(_ERASE_LINE, message))


class FileLogger(Logger):

    def __init__(self, filename, level=logging.DEBUG):
        log_handlers = [handlers.RotatingFileHandler(filename=filename, mode="a", maxBytes=1024 * 1000, backupCount=3)]
        logging.basicConfig(
            handlers=log_handlers,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            level=level)
        self.logger = logging.getLogger()

    def log(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def success(self, message):
        self.logger.info(message)

    def failure(self, message):
        self.logger.error(message)


class NoopLogger(Logger):
    def log(self, message):
        pass

    def debug(self, message):
        pass

    def info(self, message):
        pass

    def warn(self, message):
        pass

    def error(self, message):
        pass

    def success(self, message):
        pass

    def failure(self, message):
        pass


class CompositeLogger(Logger):
    def __init__(self, *loggers: Logger):
        self.loggers = loggers

    def log(self, message):
        self._all("log", message)

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

    def _all(self, fn_name, msg):
        for logger in self.loggers:
            fn = getattr(logger, fn_name)
            fn(msg)
