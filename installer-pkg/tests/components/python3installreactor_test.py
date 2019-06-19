import unittest

from inspector.api.semver import SemVer
from inspector.api.validator import ValidationResult, Status
from inspector.components.python import PythonInfo
from installer.components.python import Python3InstallReactor
from tests.testutil import test_context


class Python3InstallReactorTest(unittest.TestCase):

    def test_no_action_reaction(self):
        reactor = Python3InstallReactor()

        commands = reactor.react(validation_result_with(status=Status.OK), ctx=test_context())
        self.assertEqual(0, len(commands))

    def test_install_action_reaction(self):
        reactor = Python3InstallReactor()

        commands = reactor.react(validation_result_with(status=Status.NOT_FOUND), ctx=test_context())

        self.assertEqual(2, len(commands))

        download_command = commands[0]
        self.assertIn("curl -s", str(download_command))

        install_command = commands[1]
        self.assertIn("sudo installer", str(install_command))

    def test_upgrade_action_reaction(self):
        reactor = Python3InstallReactor()

        commands = reactor.react(validation_result_with(status=Status.UPGRADE_REQUIRED), ctx=test_context())
        self.assertEqual(0, len(commands))

    def test_downgrade_action_reaction(self):
        reactor = Python3InstallReactor()

        commands = reactor.react(validation_result_with(status=Status.DOWNGRADE_REQUIRED), ctx=test_context())
        self.assertEqual(0, len(commands))


def validation_result_with(status: Status):
    return ValidationResult(python_info_with(), status)


def python_info_with(major="0", minor="0", patch="0"):
    return PythonInfo("/", SemVer(major, minor, patch))


if __name__ == '__main__':
    unittest.main()
