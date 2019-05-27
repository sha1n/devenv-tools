from collections import namedtuple

from inspector.api.collector import Collector
from inspector.api import context
from inspector.util import cmd

DiskInfo = namedtuple(typename="DiskInfo", field_names=["filesystem", "total", "used", "free"])


class DiskInfoCollector(Collector):
    def __init__(self, ctx: context.Context):
        super().__init__(ctx)

    def collect(self):
        self.logger.info("Collecting disk information...")

        disk_line = cmd.execute(["df", "-H", "/"]).split("\n")[1].split()

        return DiskInfo(
            filesystem=disk_line[0],
            total=disk_line[1],
            used=disk_line[2],
            free=disk_line[3],
        )
