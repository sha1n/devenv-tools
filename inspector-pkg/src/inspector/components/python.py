import shutil
from collections import namedtuple

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.semver import SemVer
from inspector.api.validator import Validator, ValidationResult, Status
from inspector.util import cmd

PythonInfo = namedtuple(typename="PythonInfo", field_names=["path", "version"])
PythonInfo.__str__ = lambda self: "PythonInfo(path={}, version={})".format(self.path, self.version)


class PythonInfoCollector(Collector):
    def __init__(self, binary_name="python"):
        self.binary_name = binary_name

    def collect(self, ctx: Context):
        ctx.logger.progress("Collecting Python binary information for {}...".format(self.binary_name))
        path = shutil.which(self.binary_name)

        if path is None:
            return None  # python not found

        major, minor, patch = self._python_version()
        return PythonInfo(path, SemVer(major, minor, patch))

    def _python_version(self):
        return cmd.execute([self.binary_name, "--version"]).split()[1].split(".")


class PythonInfoValidator(Validator):
    def __init__(self, expected_ver: SemVer):
        self.expected_ver = expected_ver

    def validate(self, input_data: PythonInfo, ctx: Context) -> ValidationResult:
        if input_data is None:
            ctx.logger.warn("Python not installed!")
            return ValidationResult(input_data, Status.NOT_FOUND)

        if int(self.expected_ver.major) > int(input_data.version.major) \
                or int(self.expected_ver.minor) > int(input_data.version.minor):
            ctx.logger.warn(
                "Python upgrade required! Expected: {}, actual: {}".format(self.expected_ver, input_data.version)
            )
            return ValidationResult(input_data, Status.UPGRADE_REQUIRED)
        else:
            return ValidationResult(input_data, Status.OK)


class PythonInfoStrictValidator(Validator):
    def __init__(self, expected_ver: SemVer, strict=False):
        self.expected_ver = expected_ver
        self.strict = strict

    def validate(self, input_data: PythonInfo, ctx: Context) -> ValidationResult:
        if input_data is None:
            ctx.logger.warn("Python not installed!")
            return ValidationResult(input_data, Status.NOT_FOUND)

        if self.expected_ver != input_data.version:
            ctx.logger.warn(
                "Incompatible Python version! Expected: {}, actual: {}".format(self.expected_ver, input_data.version)
            )

            return ValidationResult(input_data, Status.NOT_FOUND)

        else:
            return ValidationResult(input_data, Status.OK)
