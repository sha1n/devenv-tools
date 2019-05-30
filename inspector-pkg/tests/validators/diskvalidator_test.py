import unittest

from inspector.api.validator import Status
from inspector.components.disk import DiskInfoValidator, DiskInfo
from tests.testutil import test_context


class DiskInfoValidatorTest(unittest.TestCase):

    def test_validate_no_data(self):
        validator = DiskInfoValidator(ctx=test_context())

        result = validator.validate(None)
        self.assertEqual(Status.ERROR, result.status)

    def test_validate_ok(self):
        validator = DiskInfoValidator(ctx=test_context())

        result = validator.validate(DiskInfo(filesystem="", total=1, used=1, free=1))
        self.assertEqual(Status.OK, result.status)

    def test_validate_low_space(self):
        validator = DiskInfoValidator(ctx=test_context())

        result = validator.validate(DiskInfo(filesystem="", total=100, used=91, free=9))
        self.assertEqual(Status.WARNING, result.status)


if __name__ == '__main__':
    unittest.main()
