from abc import abstractmethod

from inspector.api.context import Context


class Collector:
    @abstractmethod
    def collect(self, ctx: Context) -> object: pass
