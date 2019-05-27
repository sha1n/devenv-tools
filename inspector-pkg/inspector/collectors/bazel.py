from collections import namedtuple

from inspector.api.collector import Collector
from inspector.collectors.semver import SemVer
from inspector.api import context
from inspector.util import cmd

BazelInfo = namedtuple(typename="BazelInfo", field_names=["path", "real_path", "version"])


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
