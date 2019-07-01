import unittest

from shminspector.api.validator import Status
from shminspector.components.gcloud import GCloudConfigValidator, GCloudConfig
from tests.testutil import test_context


class GCloudConfigValidatorTest(unittest.TestCase):

    def test_validate_no_data(self):
        validator = GCloudConfigValidator()

        result = validator.validate(None, ctx=test_context())
        self.assertEqual(Status.NOT_FOUND, result.status)

    def test_validate_ok(self):
        validator = GCloudConfigValidator()

        result = validator.validate(
            input_data=GCloudConfig(account="gcloud@test.com", auth_ok=True, docker_ok=True),
            ctx=test_context()
        )
        self.assertEqual(Status.OK, result.status)

    def test_validate_docker_not_ok(self):
        validator = GCloudConfigValidator()

        result = validator.validate(
            GCloudConfig(account="gcloud@test.com", auth_ok=True, docker_ok=False),
            ctx=test_context()
        )
        self.assertEqual(Status.NOT_FOUND, result.status)

    def test_validate_auth_not_ok(self):
        validator = GCloudConfigValidator()

        result = validator.validate(
            GCloudConfig(account="gcloud@test.com", auth_ok=False, docker_ok=True),
            ctx=test_context()
        )
        self.assertEqual(Status.NOT_FOUND, result.status)


if __name__ == '__main__':
    unittest.main()
