import unittest

from inspector.api.validator import ValidationResult, Status
from inspector.components.bazel import BazelInfo
from inspector.components.semver import SemVer
from installer.components.bazel import BazelInstallReactor
from tests.testutil import test_context


class BazelInstallReactorTest(unittest.TestCase):

    def test_no_action_reaction(self):
        reactor = BazelInstallReactor(test_context())

        commands = reactor.react(validation_result_with(status=Status.OK))
        self.assertEqual(len(commands), 1)
        self.assertEqual("brew upgrade bazelbuild/tap/bazelisk", str(commands[0]))

    def test_install_action_reaction(self):
        reactor = BazelInstallReactor(test_context())

        commands = reactor.react(validation_result_with(status=Status.NOT_FOUND))
        self.assertEqual(len(commands), 3)
        self.assertEqual("brew tap bazelbuild/tap", str(commands[0]))
        self.assertEqual("brew tap-pin bazelbuild/tap", str(commands[1]))
        self.assertEqual("brew install bazelbuild/tap/bazelisk", str(commands[2]))

    def test_upgrade_action_reaction(self):
        reactor = BazelInstallReactor(test_context())

        commands = reactor.react(validation_result_with(status=Status.UPGRADE_REQUIRED))
        self.assertEqual(4, len(commands))
        self.assertEqual("brew uninstall bazelbuild/tap/bazel", str(commands[0]))
        self.assertEqual("brew tap bazelbuild/tap", str(commands[1]))
        self.assertEqual("brew tap-pin bazelbuild/tap", str(commands[2]))
        self.assertEqual("brew install bazelbuild/tap/bazelisk", str(commands[3]))


def validation_result_with(status: Status):
    return ValidationResult(bazel_info_with(), status)


def bazel_info_with(major="0", minor="0", patch="0"):
    return BazelInfo("/", "/", SemVer(major, minor, patch))


if __name__ == '__main__':
    unittest.main()
