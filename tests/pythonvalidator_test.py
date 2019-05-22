import unittest

from inspector.collectors.python import PythonInfo
from inspector.collectors.semver import SemVer
from inspector.commons.context import Context
from inspector.validators.python import PythonInfoValidator, Status


class TestPythonInfoValidator(unittest.TestCase):

    def test_validate(self):
        validator = PythonInfoValidator(expected_ver=expected_version(), ctx=Context(name="test"))
        python_info = python_info_with()

        result = validator.validate(python_info)
        self.assertEqual(result.status, Status.OK)

    def test_missing_python_info(self):
        validator = PythonInfoValidator(expected_ver=expected_version(), ctx=Context(name="test"))
        python_info = None

        result = validator.validate(python_info)
        self.assertEqual(result.status, Status.NOT_FOUND)

    def test_validate_patch_version_diff(self):
        validator = PythonInfoValidator(expected_ver=expected_version(), ctx=Context(name="test"))
        python_info = python_info_with(patch="1")

        result = validator.validate(python_info)
        self.assertEqual(result.status, Status.OK)

    def test_validate_minor_version_diff(self):
        validator = PythonInfoValidator(expected_ver=expected_version(), ctx=Context(name="test"))
        python_info = python_info_with(minor="12")

        result = validator.validate(python_info)
        self.assertEqual(result.status, Status.OK)

    def test_validate_incompatible_major_version(self):
        validator = PythonInfoValidator(expected_ver=expected_version(), ctx=Context(name="test"))
        python_info = python_info_with(major="1")

        result = validator.validate(python_info)
        self.assertEqual(result.status, Status.ERROR)


def python_info_with(major="2", minor="0", patch="0"):
    return PythonInfo("/", SemVer(major, minor, patch))


def expected_version(major="2", minor="0", patch="0"):
    return SemVer(major, minor, patch)


if __name__ == '__main__':
    unittest.main()
