from abc import abstractmethod
from util import context


class Collector:
    def __init__(self, ctx: context.Context):
        self.ctx = ctx
        self.logger = ctx.logger

    @abstractmethod
    def collect(self): pass
