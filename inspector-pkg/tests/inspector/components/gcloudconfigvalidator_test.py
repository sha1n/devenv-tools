import unittest

from inspector.api.validator import Status
from inspector.components.gcloud import GCloudConfigValidator, GCloudConfig
from tests.testutil import test_context


class GCloudConfigValidatorTest(unittest.TestCase):

    def test_validate_no_data(self):
        validator = GCloudConfigValidator()

        result = validator.validate(None, ctx=test_context())
        self.assertEqual(Status.NOT_FOUND, result.status)

    def test_validate_ok(self):
        validator = GCloudConfigValidator()

        result = validator.validate(GCloudConfig(account="gcloud@test.com", auth_ok=True), ctx=test_context())
        self.assertEqual(Status.OK, result.status)


if __name__ == '__main__':
    unittest.main()
