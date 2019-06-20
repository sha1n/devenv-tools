import logging
from enum import Enum

from inspector.api.platformcompatibility import CURRENT_PLATFORM
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
                 debug=False,
                 log_file=None,
                 plan=False,
                 dryrun=False,
                 mode=Mode.INTERACTIVE):
        self.name = name
        self.mode = mode
        self.debug = debug
        self.log_file_path = log_file
        self.plan = plan
        self.dryrun = dryrun
        self.registry = registry
        self.platform = CURRENT_PLATFORM

        loggers = []
        log_level = logging.DEBUG if debug else logging.INFO

        if mode == Mode.INTERACTIVE:
            loggers.append(ConsoleLogger(level=log_level))

        if log_file is not None:
            loggers.append(FileLogger(filename=self.log_file_path, level=log_level))

        self.logger = CompositeLogger(loggers)

    def __str__(self):
        return "Context(name={}, mode={}, debug={}, log_file_path={}, plan={}, dryrun={}, logger={})".format(
            self.name, self.mode, self.debug, self.log_file_path, self.plan, self.dryrun,
            self.logger.__class__.__name__)
