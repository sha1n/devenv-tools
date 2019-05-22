from util import cmd
from util import context

from .base_collector import Collector


class DiskInfo:
    def __init__(self, filesystem, total, used, free):
        self.filesystem = filesystem
        self.total = total
        self.used = used
        self.free = free

    def __str__(self):
        return "Disk Info: filesystem={}, total={}, used={}, free={}" \
            .format(self.filesystem, self.total, self.used, self.free)


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
