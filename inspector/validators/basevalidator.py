from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum

from inspector.commons.context import Context


class Status(Enum):
    OK = 0
    WARNING = 1
    ERROR = 2
    NOT_FOUND = 3
    UPGRADE_REQUIRED = 4
    DOWNGRADE_REQUIRED = 5


@dataclass
class ValidationResult:
    def __init__(self, input_data, status: Status, ctx: Context):
        self.input_data = input_data
        self.status = status
        self.ctx = ctx


class Validator:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.logger = ctx.logger

    @abstractmethod
    def validate(self, input_data) -> ValidationResult: pass
