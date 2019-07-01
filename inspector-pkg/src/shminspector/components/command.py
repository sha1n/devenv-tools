from shutil import which

from shminspector.api.context import Context
from shminspector.api.validator import ValidationResult, Status


def command_collector(executable):
    def deco(cls):
        setattr(cls, "collect", collect_for(executable))
        setattr(cls, "__str__", str_for(executable))

        return cls

    return deco


def command_validator(executable):
    def deco(cls):
        setattr(cls, "validate", validate_for(executable))
        setattr(cls, "__str__", str_for(executable))

        return cls

    return deco


def collect_for(command):
    # noinspection PyUnusedLocal
    def collect(self, ctx: Context):
        ctx.logger.progress("Detecting {} path...".format(command))
        return which(command)

    return collect


def validate_for(command):
    # noinspection PyUnusedLocal
    def validate(self, input_data, ctx: Context) -> ValidationResult:
        if input_data is None:
            ctx.logger.warn("{} not installed!".format(command))
            return ValidationResult(input_data, Status.NOT_FOUND)

        return ValidationResult(input_data, Status.OK)

    return validate


def str_for(command):
    def _str(obj):
        return "{}('{}')".format(type(obj).__name__, command)

    return _str
