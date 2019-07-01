from collections import namedtuple

from shminspector.api.collector import Collector
from shminspector.api.context import Context
from shminspector.api.tags import macos
from shminspector.api.validator import Validator, ValidationResult, Status
from shminspector.util.cmd import try_execute

XcodeInfo = namedtuple(typename="XcodeInfo", field_names=["path"])


@macos
class XcodeInfoCollector(Collector):

    def collect(self, ctx: Context):
        ctx.logger.progress("Collecting Xcode installation information...")
        path = self._xcode_path(ctx)

        if path is not None:
            return XcodeInfo(path)
        else:
            return None

    def _xcode_path(self, ctx):
        ok, code, output = try_execute(["xcode-select", "-p"], logger=ctx)

        if ok and code != 0:
            ctx.logger.warn("xcode-select returned code '{}'".format(code))
            return None

        return output.strip()


@macos
class XcodeInfoValidator(Validator):

    def validate(self, input_data: XcodeInfo, ctx: Context) -> ValidationResult:
        if input_data is None:
            ctx.logger.warn("Xcode not installed!")
            return ValidationResult(input_data, Status.NOT_FOUND)

        else:
            ctx.logger.debug("Detected Xcode path '{}'".format(input_data.path))
            return ValidationResult(input_data, Status.OK)
