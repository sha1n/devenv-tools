from dataclasses import dataclass
from enum import Enum

from .logger import Logger, ConsoleLogger, FileLogger


class Mode(Enum):
    INTERACTIVE = 0
    BACKGROUND = 1

    def __str__(self):
        switch = {
            0: "interactive",
            1: "background",
        }

        return switch.get(self.value)


@dataclass
class Context:

    logger: Logger

    def __init__(self, name, mode=Mode.INTERACTIVE):
        self.mode = mode
        if mode == Mode.INTERACTIVE:
            self.logger = ConsoleLogger()
        else:
            self.logger = FileLogger(filename="{}.log".format(name), filemode="w")

    def __str__(self):
        return "Context(mode={}, logger={})".format(self.mode, self.logger.__class__.__name__)


