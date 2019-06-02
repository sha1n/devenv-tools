import unittest

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.executor import Executor
from inspector.api.reactor import Reactor, ReactorCommand
from inspector.api.validator import Validator, ValidationResult, Status
from inspector.components.bazel import BazelInfo
from inspector.components.semver import SemVer
from tests.testutil import test_context


class ExecutorTest(unittest.TestCase):

    def test_empty(self):
        executor = Executor()

        self.assertIsNone(executor.execute(test_context()))

    def test_basic(self):
        ctx = test_context()
        handler = RecordingHandler()

        executor = Executor()
        collector = MockCollector("data")
        validator = MockValidator(result=validation_result_with("data"))
        reactor_command = ReactorCommand(cmd=["do", "nothing"])
        reactor = MockReactor(reactor_command)

        ctx.registry.register_collector("id", collector)
        ctx.registry.register_validator("id", validator)
        ctx.registry.register_reactor("id", reactor)

        executor.execute(ctx, get_handler=handler.get)

        self.assertTrue(collector.called)
        self.assertTrue(validator.called)
        self.assertTrue(reactor.called)
        self.assertEqual(reactor_command, handler.recorded[0])

    def test_flow_with_empty_reactor(self):
        ctx = test_context()
        handler = RecordingHandler()

        executor = Executor()
        reactor = MockReactor()

        ctx.registry.register_collector("id", MockCollector("data"))
        ctx.registry.register_validator("id", MockValidator(result=validation_result_with("data")))
        ctx.registry.register_reactor("id", reactor)

        executor.execute(ctx, get_handler=handler.get)

        self.assertTrue(reactor.called)
        self.assertEqual(0, len(handler.recorded))

    def test_flow_with_command_failure(self):
        ctx = test_context()
        handler = RecordingHandler(fail=True)

        executor = Executor()
        collector = MockCollector("data")
        validator = MockValidator(result=validation_result_with("data"))
        reactor = MockReactor(ctx)

        ctx.registry.register_collector("id", collector)
        ctx.registry.register_validator("id", validator)
        ctx.registry.register_reactor("id", reactor)

        def execute():
            executor.execute(ctx, get_handler=handler.get)

        self.assertRaises(Exception, execute)
        self.assertIsNotNone(handler.raised)

        self.assertTrue(collector.called)
        self.assertTrue(validator.called)
        self.assertTrue(reactor.called)

    def test_flow_with_multiple_components(self):
        ctx = test_context()
        handler = RecordingHandler(fail=True)

        executor = Executor()
        collector1 = MockCollector("comp1_data")
        collector2 = MockCollector("comp2_data")

        ctx.registry.register_collector("comp_1", collector1)
        ctx.registry.register_collector("comp_2", collector2)

        executor.execute(ctx, get_handler=handler.get)

        self.assertTrue(collector1.called)
        self.assertTrue(collector2.called)

    def test_validation_only(self):
        ctx = test_context()

        executor = Executor()
        collector = MockCollector("data")
        validator = MockValidator(result=validation_result_with("data"))

        ctx.registry.register_collector("id", collector)
        ctx.registry.register_validator("id", validator)

        executor.execute(ctx)

        self.assertTrue(collector.called)
        self.assertTrue(validator.called)

    def test_collection_only(self):
        ctx = test_context()

        executor = Executor()
        collector = MockCollector("data")

        ctx.registry.register_collector("id", collector)

        executor.execute(ctx)

        self.assertTrue(collector.called)


class MockCollector(Collector):
    def __init__(self, result):
        self.result = result
        self.called = False

    def collect(self, ctx: Context) -> object:
        self.called = True
        return self.result


class MockValidator(Validator):
    def __init__(self, result: ValidationResult):
        self.result = result
        self.called = False

    def validate(self, input_data, ctx: Context) -> ValidationResult:
        self.called = True
        if input_data == self.result.input_data:
            return self.result
        else:
            raise Exception("Unexpected input data {}".format(input_data))


class MockReactor(Reactor):
    def __init__(self, *commands):
        self.commands = commands
        self.called = False

    def react(self, data, ctx: Context):
        self.called = True
        return self.commands


class RecordingHandler:
    def __init__(self, fail=False):
        self.recorded = []
        self.fail = fail
        self.raised = None

    def handle(self, command, ctx):
        if self.fail:
            self.raised = Exception("fake")
            raise self.raised
        else:
            self.recorded.append(command)

    def get(self, ctx):
        return self.handle


def bazel_info_with(major="1", minor="24", patch="0"):
    return BazelInfo("/", "/", SemVer(major, minor, patch))


def expected_version(major="1", minor="24", patch="0"):
    return SemVer(major, minor, patch)


def validation_result_with(data, status: Status=Status.NOT_FOUND):
    return ValidationResult(data, status)


if __name__ == '__main__':
    unittest.main()
