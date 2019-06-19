from collections import namedtuple

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.validator import Validator, ValidationResult, Status
from inspector.util.cmd import try_execute

XcodeInfo = namedtuple(typename="XcodeInfo", field_names=["path"])


class XcodeInfoCollector(Collector):

    def collect(self, ctx: Context):
        ctx.logger.progress("Collecting Xcode installation information...")
        path = self._xcode_path(ctx)

        if path is not None:
            return XcodeInfo(path)
        else:
            return None

    def _xcode_path(self, ctx):
        ok, code, output = try_execute(["xcode-select", "-p"], ctx)

        if ok and code != 0:
            ctx.logger.warn("xcode-select returned code '{}'".format(code))
            return None

        return output


class XcodeInfoValidator(Validator):

    def validate(self, input_data: XcodeInfo, ctx: Context) -> ValidationResult:
        if input_data is None:
            ctx.logger.warn("Xcode not installed!")
            return ValidationResult(input_data, Status.NOT_FOUND)

        else:
            ctx.logger.debug("Detected Xcode path '{}'".format(input_data.path))
            return ValidationResult(input_data, Status.OK)
