from abc import abstractmethod
from enum import Enum

from inspector.api.context import Context


class Status(Enum):
    OK = 0
    WARNING = 1
    ERROR = 2
    NOT_FOUND = 3
    UPGRADE_REQUIRED = 4
    DOWNGRADE_REQUIRED = 5


class ValidationResult:
    def __init__(self, input_data, status: Status):
        self.input_data = input_data
        self.status = status


class Validator:
    @abstractmethod
    def validate(self, input_data, ctx: Context) -> ValidationResult: pass
