from collections import namedtuple
from shutil import disk_usage

from inspector.api import context
from inspector.api.collector import Collector

DiskInfo = namedtuple(typename="DiskInfo", field_names=["filesystem", "total", "used", "free"])


class DiskInfoCollector(Collector):
    def __init__(self, ctx: context.Context):
        super().__init__(ctx)

    def collect(self):
        self.logger.info("Collecting disk information...")

        total, used, free = disk_usage("/")

        return DiskInfo(
            filesystem="/",
            total="{}G".format(_b_to_gb(total)),
            used="{}G".format(_b_to_gb(used)),
            free="{}G".format(_b_to_gb(free)),
        )


def _b_to_gb(value):
    return int(value / (1024 ** 3))
