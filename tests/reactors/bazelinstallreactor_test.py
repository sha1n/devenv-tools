import unittest

from inspector.collectors.bazel import BazelInfo
from inspector.collectors.semver import SemVer
from inspector.commons.context import Context
from inspector.reactors.bazel import BazelValidationInstallReactor
from inspector.validators.basevalidator import ValidationResult
from inspector.validators.bazel import Status


class BazelValidationInstallReactorTest(unittest.TestCase):

    def test_no_action_reaction(self):
        reactor = BazelValidationInstallReactor(ctx())

        gen = reactor.react(validation_result_with(status=Status.OK))
        self.assertEqual(len(list(gen)), 0)

    def test_install_action_reaction(self):
        reactor = BazelValidationInstallReactor(ctx())

        gen = reactor.react(validation_result_with(status=Status.NOT_FOUND))
        commands = list(gen)

        self.assertEqual(len(commands), 1)

        install_command = commands[0]
        self.assertIn(" install", str(install_command))

    def test_upgrade_action_reaction(self):
        reactor = BazelValidationInstallReactor(ctx())

        gen = reactor.react(validation_result_with(status=Status.UPGRADE_REQUIRED))
        commands = list(gen)
        self.assertEqual(len(commands), 1)

        upgrade_command = commands[0]
        self.assertIn(" upgrade", str(upgrade_command))

    def test_downgrade_action_reaction(self):
        reactor = BazelValidationInstallReactor(ctx())

        gen = reactor.react(validation_result_with(status=Status.DOWNGRADE_REQUIRED))
        commands = list(gen)
        self.assertEqual(len(commands), 2)

        uninstall_command, install_command = commands
        self.assertIn(" uninstall", str(uninstall_command))
        self.assertIn(" install", str(install_command))


def validation_result_with(status: Status):
    return ValidationResult(bazel_info_with(), status)


def ctx():
    return Context(name="test")


def bazel_info_with(major="0", minor="0", patch="0"):
    return BazelInfo("/", "/", SemVer(major, minor, patch))


if __name__ == '__main__':
    unittest.main()
