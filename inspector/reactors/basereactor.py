from abc import abstractmethod
from typing import Generator

from inspector.commons.context import Context


class ReactorCommand:
    def __init__(self, cmd: []):
        super().__init__()
        self.cmd = cmd

    def __str__(self):
        return " ".join(self.cmd)


class Reactor:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.logger = ctx.logger

    @abstractmethod
    def react(self, data) -> Generator[ReactorCommand, None, None]: pass
