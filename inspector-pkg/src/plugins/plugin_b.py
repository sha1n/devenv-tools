from inspector.api.validator import Validator, ValidationResult, Status
from inspector.api.context import Context


class TestValidator(Validator):

    def validate(self, input_data, ctx: Context) -> ValidationResult:
        return ValidationResult(input_data, Status.OK)


def objects():
    yield TestValidator()


def component_id() -> str:
    return "component_b"
