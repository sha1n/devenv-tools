from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum

from inspector.util import context


class Status(Enum):
    OK = 0
    WARNING = 1
    ERROR = 2


@dataclass
class ValidationResult:
    def __init__(self, input_data, status: Status, ctx: context.Context):
        self.input = input_data
        self.status = status
        self.ctx = ctx


class Validator:
    def __init__(self, ctx: context.Context):
        self.ctx = ctx
        self.logger = ctx.logger

    @abstractmethod
    def validate(self, input_data): pass
