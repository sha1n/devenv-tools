from util import cmd
from util import context

from .base_collector import Collector
from .semver import SemVer


class BazelInfo:
    def __init__(self, path, real_path, version: SemVer):
        self.path = path
        self.real_path = real_path
        self.version = version

    def __str__(self):
        return "Bazel Info: path={}, real_path={}, version={}".format(self.path, self.real_path, self.version)


class BazelInfoCollector(Collector):
    def __init__(self, ctx: context.Context):
        super().__init__(ctx)

    def collect(self):
        self.logger.info("Collecting Bazel binary information...")
        path = _bazel_path()
        real_path = _bazel_real_path()
        version = _bazel_version()
        return BazelInfo(path, real_path, version)


def _bazel_version():
    version = cmd.execute(["bazel-real", "version", "--gnu_format=true"]).split("\n")[1].split()[1]
    major, minor, patch = version.split(".")
    return SemVer(major, minor, patch)


def _bazel_path():
    return cmd.execute(["which", "bazel"]).split()[0]


def _bazel_real_path():
    return cmd.execute(["which", "bazel-real"]).split()[0]
