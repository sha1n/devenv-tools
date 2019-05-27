from collections import namedtuple

from inspector.collectors.basecollector import Collector
from inspector.collectors.semver import SemVer
from inspector.commons import context
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


def _python_version():
    return cmd.execute(["python", "--version"]).split()[1].split(".")


def _python_path():
    return cmd.execute(["which", "python"]).split()[0]
