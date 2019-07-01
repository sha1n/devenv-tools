import unittest

from shminspector.api.validator import Status
from shminspector.components.xcode import XcodeInfo, XcodeInfoValidator
from tests.testutil import test_context


class XcodeInfoValidatorTest(unittest.TestCase):

    def test_validate(self):
        validator = XcodeInfoValidator()
        python_info = xcode_info()

        result = validator.validate(python_info, ctx=test_context())
        self.assertEqual(result.status, Status.OK)

    def test_missing_xcode(self):
        validator = XcodeInfoValidator()

        result = validator.validate(None, ctx=test_context())
        self.assertEqual(result.status, Status.NOT_FOUND)


def xcode_info():
    return XcodeInfo(path="/")


if __name__ == '__main__':
    unittest.main()
