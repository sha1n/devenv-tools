import unittest

from inspector.api.validator import Status
from inspector.components.bazel import BazelInfo, BazelInfoValidator
from inspector.components.semver import SemVer
from tests.testutil import test_context


class BazelInfoValidatorTest(unittest.TestCase):

    def test_validate(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=test_context())
        bazel_info = bazel_info_with(minor="24")

        result = validator.validate(bazel_info)
        self.assertEqual(result.status, Status.OK)

    def test_missing_bazel_info(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=test_context())

        result = validator.validate(None)
        self.assertEqual(result.status, Status.NOT_FOUND)

    def test_validate_patch_level_diff(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=test_context())
        bazel_info = bazel_info_with(patch="1")

        result = validator.validate(bazel_info)
        self.assertEqual(result.status, Status.OK)

    def test_validate_new_major_version(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=test_context())
        bazel_info = bazel_info_with(major="2")

        result = validator.validate(bazel_info)
        self.assertEqual(result.status, Status.DOWNGRADE_REQUIRED)

    def test_validate_new_minor_version(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=test_context())
        bazel_info = bazel_info_with(minor="25")

        result = validator.validate(bazel_info)
        self.assertEqual(result.status, Status.DOWNGRADE_REQUIRED)

    def test_validate_old_major_version(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=test_context())
        bazel_info = bazel_info_with(major="0")

        result = validator.validate(bazel_info)
        self.assertEqual(result.status, Status.UPGRADE_REQUIRED)

    def test_validate_old_minor_version(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=test_context())
        bazel_info = bazel_info_with(minor="12")

        result = validator.validate(bazel_info)
        self.assertEqual(result.status, Status.UPGRADE_REQUIRED)


def bazel_info_with(major="1", minor="24", patch="0"):
    return BazelInfo("/", "/", SemVer(major, minor, patch))


def expected_version(major="1", minor="24", patch="0"):
    return SemVer(major, minor, patch)


if __name__ == '__main__':
    unittest.main()
