from inspector.validators.basevalidator import Validator, ValidationResult, Status
from inspector.commons.context import Context


class TestValidator(Validator):

    def validate(self, input_data) -> ValidationResult:
        return ValidationResult(input_data, Status.OK)


def objects(ctx: Context):
    yield TestValidator(ctx)


def component_id() -> str:
    return "component_b"
