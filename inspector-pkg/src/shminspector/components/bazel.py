import shutil
from collections import namedtuple

from shminspector.api.collector import Collector
from shminspector.api.context import Context
from shminspector.api.semver import SemVer
from shminspector.api.tags import macos
from shminspector.api.validator import ValidationResult, Status, Validator
from shminspector.util import cmd
from shminspector.util.cmd import try_execute

BazelInfo = namedtuple(typename="BazelInfo", field_names=["path", "version", "bazelisk"])
BazelInfo.__str__ = lambda self: "BazelInfo(path={}, version={}, bazelisk={})" \
    .format(self.path, self.version, self.bazelisk)


@macos
class BazelInfoCollector(Collector):

    def collect(self, ctx: Context):
        ctx.logger.progress("Collecting Bazel binary information...")
        path = shutil.which("bazel")
        if path is None:
            return None

        version = self._bazel_version(ctx)
        bazelisk = self._bazelisk_exists(ctx)
        return BazelInfo(path, version, bazelisk)

    def _bazel_version(self, ctx):
        try:
            lines = cmd.execute(["bazel", "version", "--gnu_format=true"]).split("\n")
            version = lines[len(lines) - 2].split()[1]
            major, minor, patch = version.split(".")
            return SemVer(major, minor, patch)
        except Exception as err:
            ctx.logger.warn(err)
            return None

    def _bazelisk_exists(self, ctx):
        _, code, stdout = try_execute(["brew", "ls", "-1", "bazelisk"], logger=ctx.logger)

        return code == 0 and "bazelisk" in stdout


class BazelInfoValidator(Validator):

    def validate(self, input_data: BazelInfo, ctx: Context) -> ValidationResult:
        if input_data is None:
            ctx.logger.warn("Bazel not installed!")
            return ValidationResult(input_data, Status.NOT_FOUND)

        if input_data.bazelisk:
            return ValidationResult(input_data, Status.OK)

        ctx.logger.warn("Bazel upgrade required")
        return ValidationResult(input_data, Status.UPGRADE_REQUIRED)
