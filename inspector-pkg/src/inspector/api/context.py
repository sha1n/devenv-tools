import logging
from enum import Enum

from inspector.api.annotations import CURRENT_PLATFORM
from inspector.api.config import load
from inspector.api.registry import Registry
from inspector.util.logger import ConsoleLogger, FileLogger, CompositeLogger

_MODE_INTERACTIVE = "interactive"
_MODE_BACKGROUND = "background"


class Mode(Enum):
    INTERACTIVE = 0
    BACKGROUND = 1

    def __str__(self):
        switch = {
            0: _MODE_INTERACTIVE,
            1: _MODE_BACKGROUND,
        }

        return switch.get(self.value)

    @staticmethod
    def from_str(mode):
        switch = {
            _MODE_INTERACTIVE: Mode.INTERACTIVE,
            _MODE_BACKGROUND: Mode.BACKGROUND,
        }

        return switch.get(mode, Mode.INTERACTIVE)


class Context:
    def __init__(self,
                 name,
                 registry: Registry,
                 config_file=None,
                 debug=False,
                 experimental=False,
                 plan=False,
                 dryrun=False,
                 log_file=None,
                 mode=Mode.INTERACTIVE):
        self.name = name
        self.mode = mode
        self.log_file_path = log_file
        self.plan = plan
        self.registry = registry
        self.platform = CURRENT_PLATFORM
        self.config = load(config_file)
        self._set_flags(debug, dryrun, experimental, plan)

        loggers = []
        log_level = logging.DEBUG if debug else logging.INFO

        if mode == Mode.INTERACTIVE:
            loggers.append(ConsoleLogger(level=log_level))

        if log_file is not None:
            loggers.append(FileLogger(filename=self.log_file_path, level=logging.DEBUG))

        self.logger = CompositeLogger(loggers)

    def _set_flags(self, debug, dryrun, experimental, plan):
        flags = Flags()
        flags.debug = debug
        flags.experimental = experimental
        flags.plan = plan
        flags.dryrun = dryrun

        self.flags = flags

    def __str__(self):
        return "Context(name={name}, mode={mode}, flags={flags}, log_file_path={log_file_path}, " \
               "logger={logger_class}, config={config_json})" \
            .format(
            name=self.name,
            mode=self.mode,
            log_file_path=self.log_file_path,
            logger_class=self.logger.__class__.__name__,
            flags=str(self.flags),
            config_json=self.config,
        )


class Flags(object):
    def __str__(self):
        return str(self.__dict__)
