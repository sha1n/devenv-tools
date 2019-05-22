import logging
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

    def __init__(self, filename, filemode, level=logging.DEBUG):
        logging.basicConfig(
            filename=filename,
            filemode=filemode,
            format='[%(asctime)s] %(levelname)s:\t %(message)s',
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
