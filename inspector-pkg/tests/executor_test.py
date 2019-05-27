import unittest
from typing import Generator

from inspector.collectors.basecollector import Collector
from inspector.collectors.bazel import BazelInfo
from inspector.collectors.semver import SemVer
from inspector.commons.context import Context
from inspector.executor import Executor
from inspector.reactors.basereactor import Reactor, ReactorCommand
from inspector.validators.basevalidator import Validator, ValidationResult
from inspector.validators.bazel import Status
from tests.testutil import test_context


class ExecutorTest(unittest.TestCase):

    def test_empty(self):
        executor = Executor()

        self.assertEqual(executor.execute(test_context()), 0)

    def test_basic(self):
        ctx = test_context()
        ctx.call_index = 0

        executor = Executor()
        collector = MockCollector("data", ctx)
        validator = MockValidator(result=validation_result_with("data", Status.NOT_FOUND), ctx=ctx)
        reactor = MockReactor(ctx=ctx, command=ReactorCommand(cmd=["do", "nothing"]))

        executor.register_collector("id", collector)
        executor.register_validator("id", validator)
        executor.register_reactor("id", reactor)

        self.assertEqual(executor.execute(ctx), 0)


class MockCollector(Collector):
    def __init__(self, result, ctx: Context):
        super().__init__(ctx)
        self.result = result

    def collect(self) -> object:
        return self.result


class MockValidator(Validator):
    def __init__(self, result: ValidationResult, ctx: Context):
        super().__init__(ctx)
        self.result = result

    def validate(self, input_data) -> ValidationResult:
        if input_data == self.result.input_data:
            return self.result
        else:
            raise Exception("Unexpected input data {}".format(input_data))


class MockReactor(Reactor):
    def __init__(self, ctx, command):
        super().__init__(ctx)
        self.command = command

    def react(self, data):
        return [self.command]


def bazel_info_with(major="1", minor="24", patch="0"):
    return BazelInfo("/", "/", SemVer(major, minor, patch))


def expected_version(major="1", minor="24", patch="0"):
    return SemVer(major, minor, patch)


def validation_result_with(data, status: Status):
    return ValidationResult(data, status)


if __name__ == '__main__':
    unittest.main()
