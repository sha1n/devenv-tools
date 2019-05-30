from abc import abstractmethod
from typing import List

from inspector.api.context import Context


class ReactorCommand:
    def __init__(self, cmd, silent=False):
        super().__init__()
        self.cmd = cmd
        self.silent = silent

    def __str__(self):
        return " ".join(self.cmd)


class Reactor:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.logger = ctx.logger

    @abstractmethod
    def react(self, data) -> List[ReactorCommand]: pass
