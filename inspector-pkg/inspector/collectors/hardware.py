import multiprocessing
from collections import namedtuple

from inspector.api.collector import Collector
from inspector.api import context
from inspector.util import cmd

HardwareInfo = namedtuple(typename="HardwareInfo", field_names=["cpu_count", "total_ram"])


class HardwareInfoCollector(Collector):
    def __init__(self, ctx: context.Context):
        super().__init__(ctx)

    def collect(self):
        self.logger.info("Collecting hardware information...")
        cpu_count = multiprocessing.cpu_count()
        total_ram = _total_ram()
        return HardwareInfo(cpu_count, total_ram)


def _total_ram():
    raw_total_ram = cmd.execute(["sysctl", "hw.memsize"]).split(":")[1].strip()
    return "%dG" % (int(raw_total_ram) / (1024 * 1000 * 1024))
