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
    @abstractmethod
    def react(self, data, ctx: Context) -> List[ReactorCommand]: pass
