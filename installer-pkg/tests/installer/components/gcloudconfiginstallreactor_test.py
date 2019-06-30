import unittest

from inspector.api.context import Mode
from inspector.api.validator import ValidationResult, Status
from inspector.components.gcloud import GCloudConfig
from installer.components.gcloud import GCloudConfigInstallReactor
from tests.testutil import test_context


class GCloudConfigInstallReactorTest(unittest.TestCase):

    def test_reaction_to_status_ok(self):
        reactor = GCloudConfigInstallReactor()

        commands = reactor.react(validation_result_with(status=Status.OK), ctx=test_context())
        self.assertEqual(len(commands), 0)

    def test_reaction_to_not_found(self):
        reactor = GCloudConfigInstallReactor()

        commands = reactor.react(
            data=validation_result_with(status=Status.NOT_FOUND, docker_ok=False, auth_ok=False),
            ctx=test_context(mode=Mode.INTERACTIVE)
        )

        self.assertEqual(3, len(commands))

        config_docker_command = commands[0]
        self.assertIn("auth configure-docker", str(config_docker_command))

        login_command = commands[1]
        self.assertIn("auth login <user_input:gcloud_email>", str(login_command))

        app_default_login_command = commands[2]
        self.assertIn("auth application-default login", str(app_default_login_command))

    def test_reaction_to_not_found_docker(self):
        reactor = GCloudConfigInstallReactor()

        commands = reactor.react(
            data=validation_result_with(status=Status.NOT_FOUND, docker_ok=False),
            ctx=test_context(mode=Mode.INTERACTIVE)
        )

        self.assertEqual(1, len(commands))

        config_docker_command = commands[0]
        self.assertIn("auth configure-docker", str(config_docker_command))

    def test_reaction_to_not_found_auth(self):
        reactor = GCloudConfigInstallReactor()

        commands = reactor.react(
            data=validation_result_with(status=Status.NOT_FOUND, auth_ok=False),
            ctx=test_context(mode=Mode.INTERACTIVE)
        )

        self.assertEqual(2, len(commands))

        login_command = commands[0]
        self.assertIn("auth login <user_input:gcloud_email>", str(login_command))

        app_default_login_command = commands[1]
        self.assertIn("auth application-default login", str(app_default_login_command))


def validation_result_with(status: Status, auth_ok=True, docker_ok=True):
    return ValidationResult(GCloudConfig(account="acc", auth_ok=auth_ok, docker_ok=docker_ok), status)


if __name__ == '__main__':
    unittest.main()
