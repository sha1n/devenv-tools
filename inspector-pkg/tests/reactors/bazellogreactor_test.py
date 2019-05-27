import unittest

from inspector.components.bazel import BazelInfo, BazelValidationLogReactor
from inspector.components.semver import SemVer
from inspector.api.validator import ValidationResult, Status
from tests.testutil import test_context


class BazelValidationLogReactorTest(unittest.TestCase):

    def test_no_action_reaction(self):
        reactor = BazelValidationLogReactor(test_context())

        gen = reactor.react(validation_result_with(status=Status.OK))
        self.assertEqual(len(list(gen)), 0)

    def test_install_action_reaction(self):
        reactor = BazelValidationLogReactor(test_context())

        gen = reactor.react(validation_result_with(status=Status.NOT_FOUND))
        self.assertEqual(len(list(gen)), 0)

    def test_upgrade_action_reaction(self):
        reactor = BazelValidationLogReactor(test_context())

        gen = reactor.react(validation_result_with(status=Status.UPGRADE_REQUIRED))
        self.assertEqual(len(list(gen)), 0)

    def test_downgrade_action_reaction(self):
        reactor = BazelValidationLogReactor(test_context())

        gen = reactor.react(validation_result_with(status=Status.DOWNGRADE_REQUIRED))
        self.assertEqual(len(list(gen)), 0)


def validation_result_with(status: Status):
    return ValidationResult(bazel_info_with(), status)


def bazel_info_with(major="0", minor="0", patch="0"):
    return BazelInfo("/", "/", SemVer(major, minor, patch))


if __name__ == '__main__':
    unittest.main()