import os
import shutil
from collections import namedtuple

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.validator import ValidationResult, Status, Validator
from inspector.components.semver import SemVer
from inspector.util import cmd

BazelInfo = namedtuple(typename="BazelInfo", field_names=["path", "version", "bazelisk"])


class BazelInfoCollector(Collector):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def collect(self):
        self.logger.info("Collecting Bazel binary information...")
        path = shutil.which("bazel")
        if path is None:
            return None

        version = self._bazel_version()
        bazelisk = BazelInfoCollector._bazelisk_exists()
        return BazelInfo(path, version, bazelisk)

    def _bazel_version(self):
        try:
            version = cmd.execute(["bazel", "version", "--gnu_format=true"]).split("\n")[1].split()[1]
            major, minor, patch = version.split(".")
            return SemVer(major, minor, patch)
        except Exception as err:
            self.ctx.logger.warn(err)
            return None

    @staticmethod
    def _bazelisk_exists():
        return os.system("brew ls -1 bazelisk | grep bazelisk") == 0


class BazelInfoValidator(Validator):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def validate(self, input_data: BazelInfo) -> ValidationResult:
        if input_data is None:
            return ValidationResult(input_data, Status.NOT_FOUND)

        if input_data.bazelisk:
            return ValidationResult(input_data, Status.OK)

        return ValidationResult(input_data, Status.UPGRADE_REQUIRED)
