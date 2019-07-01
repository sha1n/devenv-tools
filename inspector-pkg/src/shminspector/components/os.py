import platform
from collections import namedtuple

from shminspector.api.collector import Collector
from shminspector.api.context import Context
from shminspector.api.semver import SemVer

OsInfo = namedtuple(typename="OsInfo", field_names=["name", "version"])


class OsInfoCollector(Collector):

    def collect(self, ctx: Context):
        ctx.logger.progress("Collecting OS information...")
        name = platform.system()
        major, minor, patch = platform.mac_ver()[0].split(".")
        return OsInfo(name, SemVer(major, minor, patch))
