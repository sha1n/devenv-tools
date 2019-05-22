import platform

from inspector.collectors.basecollector import Collector
from inspector.collectors.semver import SemVer
from inspector.commons import context


class OsInfo:
    def __init__(self, name, version: SemVer):
        self.name = name
        self.version = version

    def __str__(self):
        return "OS Info: name={}, version={}".format(self.name, self.version)


class OsInfoCollector(Collector):
    def __init__(self, ctx: context.Context):
        super().__init__(ctx)

    def collect(self):
        self.logger.info("Collecting OS information...")
        name = platform.system()
        major, minor, patch = platform.mac_ver()[0].split(".")
        return OsInfo(name, SemVer(major, minor, patch))
