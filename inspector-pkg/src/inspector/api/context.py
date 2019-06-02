import logging
from enum import Enum

from inspector.api.registry import Registry
from inspector.util.logger import ConsoleLogger, FileLogger, CompositeLogger, NOOP_LOGGER

_MODE_DEBUG = "debug"
_MODE_INTERACTIVE = "interactive"
_MODE_BACKGROUND = "background"
_MODE_SILENT = "silent"


class Mode(Enum):
    DEBUG = 0
    INTERACTIVE = 1
    BACKGROUND = 2
    SILENT = 3

    def __str__(self):
        switch = {
            0: _MODE_DEBUG,
            1: _MODE_INTERACTIVE,
            2: _MODE_BACKGROUND,
            3: _MODE_SILENT,
        }

        return switch.get(self.value)

    @staticmethod
    def from_str(mode):
        switch = {
            _MODE_DEBUG: Mode.DEBUG,
            _MODE_INTERACTIVE: Mode.INTERACTIVE,
            _MODE_BACKGROUND: Mode.BACKGROUND,
            _MODE_SILENT: Mode.SILENT,
        }

        return switch.get(mode, Mode.INTERACTIVE)


class Context:

    def __init__(self, name, registry: Registry, dryrun=False, mode=Mode.INTERACTIVE):
        self.name = name
        self.mode = mode
        self.dryrun = dryrun
        self.registry = registry
        self.log_file_path = "{}.log".format(name)

        if mode == Mode.INTERACTIVE:
            self.logger = ConsoleLogger()
        elif mode == Mode.BACKGROUND:
            self.logger = FileLogger(filename=self.log_file_path, level=logging.DEBUG)
        elif mode == Mode.DEBUG:
            self.logger = CompositeLogger(
                FileLogger(filename=self.log_file_path, level=logging.DEBUG),
                ConsoleLogger(level=logging.DEBUG)
            )
        elif mode == Mode.SILENT:
            self.logger = NOOP_LOGGER

    def __str__(self):
        return "Context(name={}, mode={}, dryrun={}, logger={})".format(
            self.name, self.mode, self.dryrun, self.logger.__class__.__name__)
