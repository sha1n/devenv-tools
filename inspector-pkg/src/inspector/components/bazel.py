import shutil
from collections import namedtuple

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.validator import ValidationResult, Status, Validator
from inspector.components.semver import SemVer
from inspector.util import cmd
from inspector.util.cmd import try_execute

BazelInfo = namedtuple(typename="BazelInfo", field_names=["path", "version", "bazelisk"])


class BazelInfoCollector(Collector):

    def collect(self, ctx: Context):
        ctx.logger.info("Collecting Bazel binary information...")
        path = shutil.which("bazel")
        if path is None:
            return None

        version = self._bazel_version(ctx)
        bazelisk = self._bazelisk_exists(ctx)
        return BazelInfo(path, version, bazelisk)

    def _bazel_version(self, ctx):
        try:
            version = cmd.execute(["bazel", "version", "--gnu_format=true"]).split("\n")[1].split()[1]
            major, minor, patch = version.split(".")
            return SemVer(major, minor, patch)
        except Exception as err:
            ctx.logger.warn(err)
            return None

    def _bazelisk_exists(self, ctx):
        _, code, stdout = try_execute(["brew", "ls", "-1", "bazelisk"], ctx.logger)

        return code == 0 and "bazelisk" in stdout


class BazelInfoValidator(Validator):

    def validate(self, input_data: BazelInfo, ctx: Context) -> ValidationResult:
        if input_data is None:
            return ValidationResult(input_data, Status.NOT_FOUND)

        if input_data.bazelisk:
            return ValidationResult(input_data, Status.OK)

        return ValidationResult(input_data, Status.UPGRADE_REQUIRED)
