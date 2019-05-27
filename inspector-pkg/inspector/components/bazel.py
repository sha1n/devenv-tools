import shutil
from collections import namedtuple

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.reactor import ReactorCommand, Reactor
from inspector.api.validator import ValidationResult, Status, Validator
from inspector.components.semver import SemVer
from inspector.util import cmd

BazelInfo = namedtuple(typename="BazelInfo", field_names=["path", "real_path", "version"])


class BazelInfoCollector(Collector):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def collect(self):
        self.logger.info("Collecting Bazel binary information...")
        path = shutil.which("bazel")
        if path is None:
            return None  # bazel not found

        real_path = shutil.which("bazel-real")
        version = self._bazel_version()
        return BazelInfo(path, real_path, version)

    @staticmethod
    def _bazel_version():
        version = cmd.execute(["bazel-real", "version", "--gnu_format=true"]).split("\n")[1].split()[1]
        major, minor, patch = version.split(".")
        return SemVer(major, minor, patch)


class BazelValidationLogReactor(Reactor):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def react(self, data: ValidationResult):
        if data.status != Status.OK:
            self.logger.warn("Incompatible Bazel version: {}".format(str(data.input_data.version)))

        return []


class BazelValidationInstallReactor(Reactor):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def react(self, data: ValidationResult):
        commands = []
        if data.status == Status.NOT_FOUND:
            commands.append(self._install())
        elif data.status == data.status.UPGRADE_REQUIRED:
            commands.append(self._upgrade())
        elif data.status == data.status.DOWNGRADE_REQUIRED:
            commands.append(self._uninstall())
            commands.append(self._install())

        return commands

    # fixme that command is not necessarily the real one
    @staticmethod
    def _install() -> ReactorCommand:
        return ReactorCommand(["brew", "install", "bazel"])

    # fixme that command is not necessarily the real one
    @staticmethod
    def _upgrade() -> ReactorCommand:
        return ReactorCommand(["brew", "upgrade", "bazel"])

    # fixme that command is not necessarily the real one
    @staticmethod
    def _uninstall() -> ReactorCommand:
        return ReactorCommand(["brew", "uninstall", "bazel"])


class BazelInfoValidator(Validator):
    def __init__(self, expected_ver: SemVer, ctx: Context):
        super().__init__(ctx)
        self.expected_ver = expected_ver

    def validate(self, input_data: BazelInfo) -> ValidationResult:
        if input_data is None:
            return ValidationResult(input_data, Status.NOT_FOUND)

        if self.expected_ver.major > input_data.version.major:
            return ValidationResult(input_data, Status.UPGRADE_REQUIRED)

        if self.expected_ver.major < input_data.version.major:
            return ValidationResult(input_data, Status.DOWNGRADE_REQUIRED)

        if self.expected_ver.minor > input_data.version.minor:
            return ValidationResult(input_data, Status.UPGRADE_REQUIRED)

        if self.expected_ver.minor < input_data.version.minor:
            return ValidationResult(input_data, Status.DOWNGRADE_REQUIRED)

        return ValidationResult(input_data, Status.OK)
