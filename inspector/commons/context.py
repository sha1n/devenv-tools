from dataclasses import dataclass
from enum import Enum

from inspector.util.logger import Logger, ConsoleLogger, FileLogger


class Mode(Enum):
    INTERACTIVE = 0
    BACKGROUND = 1

    def __str__(self):
        switch = {
            0: "interactive",
            1: "background",
        }

        return switch.get(self.value)

    @staticmethod
    def from_str(mode):
        switch = {
            "interactive": Mode.INTERACTIVE,
            "background": Mode.BACKGROUND,
        }

        return switch.get(mode, Mode.INTERACTIVE)


@dataclass
class Context:

    logger: Logger

    def __init__(self, name, mode=Mode.INTERACTIVE):
        self.mode = mode
        if mode == Mode.INTERACTIVE:
            self.logger = ConsoleLogger()
        else:
            self.logger = FileLogger(filename="{}.log".format(name))

    def __str__(self):
        return "Context(mode={}, logger={})".format(self.mode, self.logger.__class__.__name__)


