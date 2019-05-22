from inspector.collectors.bazel import BazelInfo
from inspector.collectors.semver import SemVer
from inspector.commons import context

from inspector.validators.basevalidator import Validator, ValidationResult, Status


class BazelInfoValidator(Validator):
    def __init__(self, expected_ver: SemVer, ctx: context.Context):
        super().__init__(ctx)
        self.expected_ver = expected_ver

    def validate(self, input_data: BazelInfo) -> ValidationResult:
        if input_data is None:
            return ValidationResult(input_data, Status.NOT_FOUND, self.ctx)

        if self.expected_ver.major > input_data.version.major:
            return ValidationResult(input_data, Status.UPGRADE_REQUIRED, self.ctx)

        if self.expected_ver.major < input_data.version.major:
            return ValidationResult(input_data, Status.DOWNGRADE_REQUIRED, self.ctx)

        if self.expected_ver.minor > input_data.version.minor:
            return ValidationResult(input_data, Status.UPGRADE_REQUIRED, self.ctx)

        if self.expected_ver.minor < input_data.version.minor:
            return ValidationResult(input_data, Status.DOWNGRADE_REQUIRED, self.ctx)

        return ValidationResult(input_data, Status.OK, self.ctx)
