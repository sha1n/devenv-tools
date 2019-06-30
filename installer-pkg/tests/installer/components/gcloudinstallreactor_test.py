import unittest

from inspector.api.context import Mode
from inspector.api.validator import ValidationResult, Status
from installer.components.gcloud import GCloudInstallReactor
from tests.testutil import test_context


class GCloudInstallReactorTest(unittest.TestCase):

    def test_reaction_to_status_ok(self):
        reactor = GCloudInstallReactor()

        commands = reactor.react(validation_result_with(status=Status.OK), ctx=test_context())
        self.assertEqual(len(commands), 0)

    def test_reaction_to_not_found(self):
        reactor = GCloudInstallReactor()

        commands = reactor.react(
            data=validation_result_with(status=Status.NOT_FOUND),
            ctx=test_context(mode=Mode.INTERACTIVE)
        )

        self.assertEqual(1, len(commands))

        install_command = commands[0]
        self.assertIn(" install", str(install_command))


def validation_result_with(status: Status):
    return ValidationResult(None, status)


if __name__ == '__main__':
    unittest.main()
