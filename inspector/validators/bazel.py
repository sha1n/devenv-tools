from inspector.collectors.bazel import BazelInfo
from inspector.collectors.semver import SemVer
from inspector.util import context

from .basevalidator import Validator, ValidationResult, Status


class BazelInfoValidator(Validator):
    def __init__(self, expected_ver: SemVer, ctx: context.Context):
        super().__init__(ctx)
        self.expected_ver = expected_ver

    def validate(self, input_data: BazelInfo) -> ValidationResult:
        if self.expected_ver.major != input_data.version.major or self.expected_ver.minor != input_data.version.minor:
            return ValidationResult(input_data, Status.ERROR, self.ctx)
        else:
            return ValidationResult(input_data, Status.OK, self.ctx)
