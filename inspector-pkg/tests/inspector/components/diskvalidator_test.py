import unittest

from shminspector.api.validator import Status
from shminspector.components.disk import DiskInfoValidator, DiskInfo
from tests.testutil import test_context


class DiskInfoValidatorTest(unittest.TestCase):

    def test_validate_no_data(self):
        validator = DiskInfoValidator()

        result = validator.validate(None, ctx=test_context())
        self.assertEqual(Status.ERROR, result.status)

    def test_validate_ok(self):
        validator = DiskInfoValidator()

        result = validator.validate(DiskInfo(filesystem="", total=1, used=1, free=1), ctx=test_context())
        self.assertEqual(Status.OK, result.status)

    def test_validate_low_space(self):
        validator = DiskInfoValidator()

        result = validator.validate(DiskInfo(filesystem="", total=100, used=91, free=9), ctx=test_context())
        self.assertEqual(Status.WARNING, result.status)


if __name__ == '__main__':
    unittest.main()
