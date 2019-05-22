import unittest

from inspector.collectors.bazel import BazelInfo
from inspector.collectors.semver import SemVer
from inspector.util.context import Context
from inspector.validators.bazel import BazelInfoValidator, Status


class TestBazelInfoValidator(unittest.TestCase):

    def test_validate(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=Context(name="test"))
        bazel_info = bazel_info_with(minor="24")

        result = validator.validate(bazel_info)
        self.assertEqual(result.status, Status.OK)

    def test_validate_patch_level_diff(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=Context(name="test"))
        bazel_info = bazel_info_with(patch="1")

        result = validator.validate(bazel_info)
        self.assertEqual(result.status, Status.OK)

    def test_validate_incompatible_major_version(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=Context(name="test"))
        bazel_info = bazel_info_with(major="1")

        result = validator.validate(bazel_info)
        self.assertEqual(result.status, Status.ERROR)

    def test_validate_incompatible_minor_version(self):
        validator = BazelInfoValidator(expected_ver=expected_version(), ctx=Context(name="test"))
        bazel_info = bazel_info_with(minor="12")

        result = validator.validate(bazel_info)
        self.assertEqual(result.status, Status.ERROR)


def bazel_info_with(major="0", minor="24", patch="0"):
    return BazelInfo("/", "/", SemVer(major, minor, patch))


def expected_version(major="0", minor="24", patch="0"):
    return SemVer(major, minor, patch)


if __name__ == '__main__':
    unittest.main()
