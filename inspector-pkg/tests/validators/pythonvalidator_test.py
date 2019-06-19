import unittest

from inspector.api.validator import Status
from inspector.components.python import PythonInfo, PythonInfoValidator
from inspector.api.semver import SemVer
from tests.testutil import test_context


class PythonInfoValidatorTest(unittest.TestCase):

    def test_validate(self):
        validator = PythonInfoValidator(expected_ver=expected_version())
        python_info = python_info_with()

        result = validator.validate(python_info, ctx=test_context())
        self.assertEqual(result.status, Status.OK)

    def test_missing_python_info(self):
        validator = PythonInfoValidator(expected_ver=expected_version())

        result = validator.validate(None, ctx=test_context())
        self.assertEqual(result.status, Status.NOT_FOUND)

    def test_validate_patch_version_diff(self):
        validator = PythonInfoValidator(expected_ver=expected_version())
        python_info = python_info_with(patch="1")

        result = validator.validate(python_info, ctx=test_context())
        self.assertEqual(result.status, Status.OK)

    def test_validate_minor_version_diff(self):
        validator = PythonInfoValidator(expected_ver=expected_version())
        python_info = python_info_with(minor="12")

        result = validator.validate(python_info, ctx=test_context())
        self.assertEqual(result.status, Status.OK)

    def test_validate_incompatible_minor_version(self):
        validator = PythonInfoValidator(expected_ver=expected_version(minor="1"))
        python_info = python_info_with()

        result = validator.validate(python_info, ctx=test_context())
        self.assertEqual(result.status, Status.UPGRADE_REQUIRED)

    def test_validate_incompatible_major_version(self):
        validator = PythonInfoValidator(expected_ver=expected_version())
        python_info = python_info_with(major="1")

        result = validator.validate(python_info, ctx=test_context())
        self.assertEqual(result.status, Status.UPGRADE_REQUIRED)


def python_info_with(major="2", minor="0", patch="0"):
    return PythonInfo("/", SemVer(major, minor, patch))


def expected_version(major="2", minor="0", patch="0"):
    return SemVer(major, minor, patch)


if __name__ == '__main__':
    unittest.main()
