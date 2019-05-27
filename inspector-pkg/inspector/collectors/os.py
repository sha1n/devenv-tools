import platform
from collections import namedtuple

from inspector.api.collector import Collector
from inspector.collectors.semver import SemVer
from inspector.api import context

OsInfo = namedtuple(typename="OsInfo", field_names=["name", "version"])


class OsInfoCollector(Collector):
    def __init__(self, ctx: context.Context):
        super().__init__(ctx)

    def collect(self):
        self.logger.info("Collecting OS information...")
        name = platform.system()
        major, minor, patch = platform.mac_ver()[0].split(".")
        return OsInfo(name, SemVer(major, minor, patch))
