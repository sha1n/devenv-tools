import unittest

from inspector.components.bazel import BazelInfo, BazelValidationInstallReactor
from inspector.components.semver import SemVer
from inspector.api.validator import ValidationResult, Status
from tests.testutil import test_context


class BazelValidationInstallReactorTest(unittest.TestCase):

    def test_no_action_reaction(self):
        reactor = BazelValidationInstallReactor(test_context())

        commands = reactor.react(validation_result_with(status=Status.OK))
        self.assertEqual(len(commands), 0)

    def test_install_action_reaction(self):
        reactor = BazelValidationInstallReactor(test_context())

        commands = reactor.react(validation_result_with(status=Status.NOT_FOUND))

        self.assertEqual(len(commands), 1)

        install_command = commands[0]
        self.assertIn(" install", str(install_command))

    def test_upgrade_action_reaction(self):
        reactor = BazelValidationInstallReactor(test_context())

        commands = reactor.react(validation_result_with(status=Status.UPGRADE_REQUIRED))
        self.assertEqual(len(commands), 1)

        upgrade_command = commands[0]
        self.assertIn(" upgrade", str(upgrade_command))

    def test_downgrade_action_reaction(self):
        reactor = BazelValidationInstallReactor(test_context())

        commands = reactor.react(validation_result_with(status=Status.DOWNGRADE_REQUIRED))
        self.assertEqual(len(commands), 2)

        uninstall_command, install_command = commands
        self.assertIn(" uninstall", str(uninstall_command))
        self.assertIn(" install", str(install_command))


def validation_result_with(status: Status):
    return ValidationResult(bazel_info_with(), status)


def bazel_info_with(major="0", minor="0", patch="0"):
    return BazelInfo("/", "/", SemVer(major, minor, patch))


if __name__ == '__main__':
    unittest.main()
