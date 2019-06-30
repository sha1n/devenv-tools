import unittest
from unittest import mock
from uuid import uuid4

from inspector.api.context import Mode
from inspector.api.reactor import ReactorCommand, UserInput
from inspector.api.validator import ValidationResult, Status
from tests.testutil import test_context

expected_user_input = str(uuid4())


# noinspection PyUnusedLocal
def fake_input(prompt):
    return str(expected_user_input)


class ReactorCommandTest(unittest.TestCase):

    # noinspection PyUnusedLocal
    @mock.patch("builtins.input", side_effect=fake_input)
    def test_command_with_user_input(self, patched_input):
        command = ReactorCommand(cmd=["cmd", UserInput("x", "test: ")])

        self.assertEqual(["cmd", expected_user_input], command.resolve(ctx=test_context(mode=Mode.INTERACTIVE)))

    def test_command_with_no_user_input(self):
        expected_command = ["cmd", "--arg"]
        command = ReactorCommand(cmd=expected_command)

        self.assertEqual(expected_command, command.resolve(ctx=test_context(mode=Mode.INTERACTIVE)))


def validation_result_with(status: Status):
    return ValidationResult(None, status)


if __name__ == '__main__':
    unittest.main()
