import multiprocessing
from collections import namedtuple

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.platformcompatibility import macos
from inspector.api.validator import Validator, ValidationResult, Status
from inspector.util import cmd

HardwareInfo = namedtuple(typename="HardwareInfo", field_names=["cpu_count", "total_ram"])


@macos  # remove after fixing ram calculation method
class HardwareInfoCollector(Collector):

    def collect(self, ctx: Context):
        ctx.logger.progress("Collecting hardware information...")
        cpu_count = multiprocessing.cpu_count()
        total_ram = _total_ram()
        return HardwareInfo(cpu_count, total_ram)


class HardwareInfoValidator(Validator):

    def validate(self, input_data: HardwareInfo, ctx: Context) -> ValidationResult:
        if input_data is None:
            return ValidationResult(input_data, Status.ERROR)

        minimum_cpu_count = ctx.config["hardware"]["minimum_cpu_count"]
        if input_data.cpu_count < minimum_cpu_count:
            ctx.logger.warn("If you are using Bazel regularly, {} CPUs is suboptimal".format(input_data.cpu_count))

        minimum_total_ram_gb = ctx.config["hardware"]["minimum_total_ram_gb"]
        if input_data.total_ram < minimum_total_ram_gb:
            ctx.logger.warn("If you are using Bazel regularly, {}G RAM is suboptimal".format(input_data.total_ram))

        return ValidationResult(input_data, Status.OK)


def _total_ram():  # fixme shai: replace with a linux compatible code and remove the annotation
    raw_total_ram = cmd.execute(["sysctl", "hw.memsize"]).split(":")[1].strip()
    return int(int(raw_total_ram) / (1024 * 1000 * 1024))
