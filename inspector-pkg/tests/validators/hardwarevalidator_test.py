import unittest

from inspector.api.validator import Status
from inspector.components.hardware import HardwareInfoValidator, HardwareInfo
from tests.testutil import test_context


class DiskInfoValidatorTest(unittest.TestCase):

    def test_validate_no_data(self):
        validator = HardwareInfoValidator(ctx=test_context())

        result = validator.validate(None)
        self.assertEqual(Status.ERROR, result.status)

    def test_validate_ok(self):
        validator = HardwareInfoValidator(ctx=test_context())

        result = validator.validate(HardwareInfo(cpu_count=1, total_ram=1))
        self.assertEqual(Status.OK, result.status)


if __name__ == '__main__':
    unittest.main()
