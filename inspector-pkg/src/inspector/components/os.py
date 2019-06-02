import platform
from collections import namedtuple

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.components.semver import SemVer

OsInfo = namedtuple(typename="OsInfo", field_names=["name", "version"])


class OsInfoCollector(Collector):

    def collect(self, ctx: Context):
        ctx.logger.info("Collecting OS information...")
        name = platform.system()
        major, minor, patch = platform.mac_ver()[0].split(".")
        return OsInfo(name, SemVer(major, minor, patch))
