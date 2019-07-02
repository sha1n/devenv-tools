import unittest

from tests.testutil import test_context
from shminspector.api.context import Mode
from shminspector.api.validator import ValidationResult, Status
from shminstaller.components.docker import DockerInstallReactor


class DockerInstallReactorTest(unittest.TestCase):

    def test_reaction_to_status_ok(self):
        reactor = DockerInstallReactor()

        commands = reactor.react(validation_result_with(status=Status.OK), ctx=test_context())
        self.assertEqual(len(commands), 0)

    def test_reaction_to_not_found(self):
        reactor = DockerInstallReactor()

        commands = reactor.react(
            data=validation_result_with(status=Status.NOT_FOUND),
            ctx=test_context(mode=Mode.INTERACTIVE)
        )

        self.assertEqual(3, len(commands))

        download_command = commands[0]
        self.assertIn("curl -s --compressed -o", str(download_command))

        mount_command = commands[1]
        self.assertIn("sudo hdiutil attach ", str(mount_command))

        copy_command = commands[2]
        self.assertIn("cp -r ", str(copy_command))


def validation_result_with(status: Status):
    return ValidationResult(None, status)


if __name__ == '__main__':
    unittest.main()
