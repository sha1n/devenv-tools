from collections import namedtuple
from shutil import disk_usage

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.validator import Validator, ValidationResult, Status

DiskInfo = namedtuple(typename="DiskInfo", field_names=["filesystem", "total", "used", "free"])


class DiskInfoCollector(Collector):

    def collect(self, ctx: Context):
        ctx.logger.info("Collecting disk information...")

        total, used, free = disk_usage("/")

        return DiskInfo(
            filesystem="/",
            total=_b_to_gb(total),
            used=_b_to_gb(used),
            free=_b_to_gb(free),
        )


class DiskInfoValidator(Validator):

    def validate(self, input_data: DiskInfo, ctx: Context) -> ValidationResult:
        if input_data is None:
            ctx.logger.error("No disk space info!")
            return ValidationResult(input_data, Status.ERROR)

        free_ratio = input_data.free / input_data.total
        if free_ratio < 0.1:
            free_percent = int(free_ratio * 100)
            ctx.logger.warn("Low disk space on filesystem '{}' ({}% free)".format(
                input_data.filesystem,
                free_percent)
            )

            return ValidationResult(input_data, Status.WARNING)

        return ValidationResult(input_data, Status.OK)


def _b_to_gb(value):
    return int(value / (1024 ** 3))
