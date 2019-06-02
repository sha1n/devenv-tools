from inspector.api.validator import Validator, ValidationResult, Status
from inspector.api.collector import Collector
from inspector.api.context import Context


class TestValidator(Validator):

    def validate(self, input_data, ctx: Context) -> ValidationResult:
        ctx.logger.info("Validating [{}]...".format(input_data))
        return ValidationResult(input_data, Status.OK)


class TestCollector(Collector):

    def collect(self, ctx: Context) -> object:
        ctx.logger.info("Collecting data for [{}]...".format(component_id()))
        return "Data from {}".format(component_id())


def objects():
    yield TestCollector()
    yield TestValidator()


def component_id() -> str:
    return "component_a"
