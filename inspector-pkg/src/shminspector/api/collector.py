from abc import abstractmethod

from shminspector.api.context import Context


class Collector:
    @abstractmethod
    def collect(self, ctx: Context) -> object: pass
