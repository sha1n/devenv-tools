from abc import abstractmethod
from typing import List

from inspector.api.context import Context


class UserInput:
    def __init__(self, key, prompt):
        self.key = key
        self.prompt = prompt

    def __str__(self):
        return "<user_input:{}>".format(self.key)


class ReactorCommand:
    def __init__(self, cmd, silent=False):
        """
        :param cmd: a list of either strings or UserInput instances
        :param silent: True if this command output should not be printed to the console, otherwise False (default)
        """
        self._cmd = cmd
        self.silent = silent

    def resolve(self, ctx: Context):
        resolved_cmd = []

        for value in self._cmd:
            if type(value) == UserInput:
                resolved_cmd.append(ctx.get_or_request_user_input(value.key, value.prompt))
            else:
                resolved_cmd.append(value)

        return resolved_cmd

    def __str__(self):
        return " ".join((str(s) for s in self._cmd))


class Reactor:
    @abstractmethod
    def react(self, data, ctx: Context) -> List[ReactorCommand]: pass
