from inspector.collectors.python import PythonInfo
from inspector.collectors.semver import SemVer
from inspector.commons import context

from inspector.validators.basevalidator import Validator, ValidationResult, Status


class PythonInfoValidator(Validator):
    def __init__(self, expected_ver: SemVer, ctx: context.Context):
        super().__init__(ctx)
        self.expected_ver = expected_ver

    def validate(self, input_data: PythonInfo) -> ValidationResult:
        if input_data is None:
            return ValidationResult(input_data, Status.NOT_FOUND, self.ctx)

        if self.expected_ver.major != input_data.version.major:
            return ValidationResult(input_data, Status.ERROR, self.ctx)
        else:
            return ValidationResult(input_data, Status.OK, self.ctx)
