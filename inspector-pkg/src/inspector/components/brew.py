from shutil import which

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.platformcompatibility import macos
from inspector.api.validator import Validator, ValidationResult, Status


@macos
class HomebrewCollector(Collector):

    def collect(self, ctx: Context):
        ctx.logger.progress("Detecting homebrew path...")
        return which("brew")


@macos
class HomebrewValidator(Validator):

    def validate(self, input_data, ctx: Context) -> ValidationResult:
        if input_data is None:
            ctx.logger.warn("Homebrew not installed!")
            return ValidationResult(input_data, Status.NOT_FOUND)

        return ValidationResult(input_data, Status.OK)
