from inspector.collectors.bazel import BazelInfo
from inspector.collectors.semver import SemVer
from inspector.api import context

from inspector.api.validator import Validator, ValidationResult, Status


class BazelInfoValidator(Validator):
    def __init__(self, expected_ver: SemVer, ctx: context.Context):
        super().__init__(ctx)
        self.expected_ver = expected_ver

    def validate(self, input_data: BazelInfo) -> ValidationResult:
        if input_data is None:
            return ValidationResult(input_data, Status.NOT_FOUND)

        if self.expected_ver.major > input_data.version.major:
            return ValidationResult(input_data, Status.UPGRADE_REQUIRED)

        if self.expected_ver.major < input_data.version.major:
            return ValidationResult(input_data, Status.DOWNGRADE_REQUIRED)

        if self.expected_ver.minor > input_data.version.minor:
            return ValidationResult(input_data, Status.UPGRADE_REQUIRED)

        if self.expected_ver.minor < input_data.version.minor:
            return ValidationResult(input_data, Status.DOWNGRADE_REQUIRED)

        return ValidationResult(input_data, Status.OK)
