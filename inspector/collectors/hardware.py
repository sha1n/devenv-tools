import multiprocessing

from util import cmd
from util import context

from .base_collector import Collector


class HardwareInfo:
    def __init__(self, cpu_count, total_ram):
        self.cpu_count = cpu_count
        self.total_ram = total_ram

    def __str__(self):
        return "Hardware Info: cpu_count={}, total_ram={}".format(self.cpu_count, self.total_ram)


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
