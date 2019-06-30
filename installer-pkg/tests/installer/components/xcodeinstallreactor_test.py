import unittest

from inspector.api.context import Mode
from inspector.api.validator import ValidationResult, Status
from inspector.components.xcode import XcodeInfo
from installer.components.xcode import XcodeInstallReactor
from tests.testutil import test_context


class XcodeValidationInstallReactorTest(unittest.TestCase):

    def test_ok_reaction(self):
        reactor = XcodeInstallReactor()

        commands = reactor.react(validation_result_with(status=Status.OK), ctx=interactive_context())
        self.assertEqual(0, len(commands))

    def test_not_found_reaction(self):
        reactor = XcodeInstallReactor()

        commands = reactor.react(validation_result_with(status=Status.NOT_FOUND),
                                 ctx=test_context(mode=Mode.INTERACTIVE))

        self.assertEqual(1, len(commands))

        install_command = commands[0]
        self.assertEqual("xcode-select --install", str(install_command))

    def test_upgrade_reaction(self):
        reactor = XcodeInstallReactor()

        commands = reactor.react(validation_result_with(status=Status.UPGRADE_REQUIRED), ctx=interactive_context())
        self.assertEqual(0, len(commands))

    def test_downgrade_reaction(self):
        reactor = XcodeInstallReactor()

        commands = reactor.react(validation_result_with(status=Status.DOWNGRADE_REQUIRED), ctx=interactive_context())
        self.assertEqual(0, len(commands))


def interactive_context():
    return test_context(mode=Mode.INTERACTIVE)


def validation_result_with(status: Status):
    return ValidationResult(XcodeInfo(path="/"), status)


if __name__ == '__main__':
    unittest.main()
