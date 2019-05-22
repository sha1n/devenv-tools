from abc import abstractmethod

from inspector.commons.context import Context


class Reactor:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.logger = ctx.logger

    @abstractmethod
    def react(self, data): pass
