import unittest

from shminspector.api.semver import SemVer
from shminspector.api.validator import Status
from shminspector.components.python import PythonInfo, PythonInfoStrictValidator
from tests.testutil import test_context


class PythonInfoStrictValidatorTest(unittest.TestCase):

    def test_validate(self):
        validator = PythonInfoStrictValidator(expected_ver=expected_version())
        python_info = python_info_with()

        result = validator.validate(python_info, ctx=test_context())
        self.assertEqual(Status.OK, result.status)

    def test_missing_python_info(self):
        validator = PythonInfoStrictValidator(expected_ver=expected_version())

        result = validator.validate(None, ctx=test_context())
        self.assertEqual(Status.NOT_FOUND, result.status)

    def test_validate_patch_version_diff(self):
        validator = PythonInfoStrictValidator(expected_ver=expected_version())
        python_info = python_info_with(patch="1")

        result = validator.validate(python_info, ctx=test_context())
        self.assertEqual(Status.NOT_FOUND, result.status)

    def test_validate_minor_version_diff(self):
        validator = PythonInfoStrictValidator(expected_ver=expected_version())
        python_info = python_info_with(minor="12")

        result = validator.validate(python_info, ctx=test_context())
        self.assertEqual(Status.NOT_FOUND, result.status)

    def test_validate_major_version_diff(self):
        validator = PythonInfoStrictValidator(expected_ver=expected_version())
        python_info = python_info_with(major="3")

        result = validator.validate(python_info, ctx=test_context())
        self.assertEqual(Status.NOT_FOUND, result.status)


def python_info_with(major="2", minor="0", patch="0"):
    return PythonInfo("/", SemVer(major, minor, patch))


def expected_version(major="2", minor="0", patch="0"):
    return SemVer(major, minor, patch)


if __name__ == '__main__':
    unittest.main()
