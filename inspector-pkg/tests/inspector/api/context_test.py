import unittest
from unittest import mock
from uuid import uuid4

from inspector.api.context import Context, Mode
from inspector.api.registry import Registry

random_user_input = uuid4()


# noinspection PyUnusedLocal
def fake_input(prompt):
    return random_user_input


class ContextTest(unittest.TestCase):

    def test_user_input_fails_in_non_interactive_mode(self):
        context = Context(name="test", registry=Registry(), mode=Mode.BACKGROUND)

        self.assertRaises(Exception, lambda *args: context.get_or_request_user_input("any", "some prompt"))

    def test_existing_user_input(self):
        context = Context(name="test", registry=Registry(), mode=Mode.INTERACTIVE)
        key = uuid4()
        value = uuid4()

        context._user_inputs[key] = value

        self.assertEqual(value, context.get_or_request_user_input(key, "some prompt"))

    # noinspection PyUnusedLocal
    @mock.patch("builtins.input", side_effect=fake_input)
    def test_prompt_with_non_existing_user_input(self, patched_input):
        context = Context(name="test", registry=Registry(), mode=Mode.INTERACTIVE)
        key = uuid4()

        self.assertEqual(random_user_input, context.get_or_request_user_input(key, "some prompt"))


if __name__ == '__main__':
    unittest.main()
