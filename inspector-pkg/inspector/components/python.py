from collections import namedtuple

from inspector.api import context
from inspector.api.collector import Collector
from inspector.api.validator import Validator, ValidationResult, Status
from inspector.components.semver import SemVer
from inspector.util import cmd

PythonInfo = namedtuple(typename="PythonInfo", field_names=["path", "version"])


class PythonInfoCollector(Collector):
    def __init__(self, ctx: context.Context):
        super().__init__(ctx)

    def collect(self):
        self.logger.info("Collecting Python binary information...")
        path = _python_path()
        major, minor, patch = _python_version()
        return PythonInfo(path, SemVer(major, minor, patch))


class PythonInfoValidator(Validator):
    def __init__(self, expected_ver: SemVer, ctx: context.Context):
        super().__init__(ctx)
        self.expected_ver = expected_ver

    def validate(self, input_data: PythonInfo) -> ValidationResult:
        if input_data is None:
            return ValidationResult(input_data, Status.NOT_FOUND)

        if self.expected_ver.major != input_data.version.major:
            return ValidationResult(input_data, Status.ERROR)
        else:
            return ValidationResult(input_data, Status.OK)


def _python_version():
    return cmd.execute(["python", "--version"]).split()[1].split(".")


def _python_path():
    return cmd.execute(["which", "python"]).split()[0]
