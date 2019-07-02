from collections import namedtuple
from os.path import exists

from shminspector.api.collector import Collector
from shminspector.api.context import Context
from shminspector.api.tags import macos
from shminspector.api.validator import Validator, ValidationResult, Status

DockerInfo = namedtuple(typename="DockerInfo", field_names=["d4m_installed"])

@macos
class DockerInfoCollector(Collector):

    def collect(self, ctx: Context):
        ctx.logger.progress("Detecting Docker Desktop information...")

        return DockerInfo(
            d4m_installed=exists("/Applications/Docker.app")
        )

@macos
class DockerInfoValidator(Validator):

    def validate(self, input_data: DockerInfo, ctx: Context) -> ValidationResult:
        if input_data is None:
            return ValidationResult(input_data, Status.ERROR)

        if not input_data.d4m_installed:
            ctx.logger.warn("Docker Desktop not installed!")
            return ValidationResult(input_data, Status.NOT_FOUND)

        return ValidationResult(input_data, Status.OK)
