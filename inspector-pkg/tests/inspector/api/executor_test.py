import unittest

from shminspector.api.collector import Collector
from shminspector.api.context import Context, Mode
from shminspector.api.executor import Executor, ExecutionSummary, ExecPlanExecutor
from shminspector.api.reactor import Reactor, ReactorCommand
from shminspector.api.tags import experimental, CURRENT_PLATFORM, Platform, target_platform, interactive
from shminspector.api.validator import Validator, ValidationResult, Status
from tests.testutil import test_context


class ExecutorTest(unittest.TestCase):

    def test_empty_execute(self):
        executor = Executor()

        self.assertEqual(ExecutionSummary(0, 0), executor.execute(test_context()))

    def test_basic_execute(self):
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

        self.assertEqual(
            ExecutionSummary(total_count=1, problem_count=1),
            executor.execute(ctx, get_handler=handler.get)
        )

        self.assertTrue(collector.called)
        self.assertTrue(validator.called)
        self.assertTrue(reactor.called)
        self.assertEqual(reactor_command, handler.recorded[0])

    def test_execute_flow_with_empty_reactor(self):
        ctx = test_context()
        handler = RecordingHandler()

        executor = Executor()
        reactor = MockReactor()

        ctx.registry.register_collector("id", MockCollector("data"))
        ctx.registry.register_validator("id", MockValidator(result=validation_result_with("data")))
        ctx.registry.register_reactor("id", reactor)

        self.assertEqual(
            ExecutionSummary(total_count=1, problem_count=1),
            executor.execute(ctx, get_handler=handler.get)
        )

        self.assertTrue(reactor.called)
        self.assertEqual(0, len(handler.recorded))

    def test_execute_flow_with_command_failure(self):
        ctx = test_context()
        handler = RecordingHandler(fail=True)

        executor = Executor()
        collector = MockCollector("data")
        validator = MockValidator(result=validation_result_with("data"))
        reactor = MockReactor("whatever")

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

    def test_execute_flow_with_multiple_components(self):
        ctx = test_context()
        handler = RecordingHandler(fail=True)

        executor = Executor()
        collector1 = MockCollector("comp1_data")
        collector2 = MockCollector("comp2_data")

        ctx.registry.register_collector("comp_1", collector1)
        ctx.registry.register_collector("comp_2", collector2)

        self.assertEqual(
            ExecutionSummary(total_count=2, problem_count=0),
            executor.execute(ctx, get_handler=handler.get)
        )

        self.assertTrue(collector1.called)
        self.assertTrue(collector2.called)

    def test_execute_validation_only(self):
        ctx = test_context()

        executor = Executor()
        collector = MockCollector("data")
        validator = MockValidator(result=validation_result_with("data"))

        ctx.registry.register_collector("id", collector)
        ctx.registry.register_validator("id", validator)

        self.assertEqual(ExecutionSummary(total_count=1, problem_count=1), executor.execute(ctx))

        self.assertTrue(collector.called)
        self.assertTrue(validator.called)

    def test_execute_collection_only(self):
        ctx = test_context()

        executor = Executor()
        collector = MockCollector("data")

        ctx.registry.register_collector("id", collector)

        self.assertEqual(ExecutionSummary(total_count=1, problem_count=0), executor.execute(ctx))

        self.assertTrue(collector.called)

    def test_experimental_component_not_executed(self):
        ctx = test_context()
        ctx.flags.experimental = False

        executor = Executor()
        collector = ExperimentalMockCollector()

        ctx.registry.register_collector("id", collector)

        executor.execute(ctx)

        self.assertFalse(collector.called)

    def test_experimental_component_executed_when_experimental_flag_is_on(self):
        ctx = test_context()
        ctx.flags.experimental = True

        executor = Executor()
        collector = ExperimentalMockCollector()

        ctx.registry.register_collector("id", collector)

        executor.execute(ctx)

        self.assertTrue(collector.called)

    def test_platform_incompatible_component_not_executed(self):
        ctx = test_context()

        executor = Executor()
        collector = PlatformInCompatible()

        ctx.registry.register_collector("id", collector)

        executor.execute(ctx)

        self.assertFalse(collector.called)

    def test_interactive_component_not_executed_in_non_interactive_mode(self):
        ctx = test_context(mode=Mode.BACKGROUND)

        executor = Executor()
        collector = InteractiveMockCollector()

        ctx.registry.register_collector("id", collector)

        executor.execute(ctx)

        self.assertFalse(collector.called)

    def test_filtered_component_list(self):
        ctx = test_context(mode=Mode.BACKGROUND)
        ctx.components = ["id1", "id3"]

        executor = Executor()
        collector1 = MockCollector("data")
        collector2 = MockCollector("data")
        collector3 = MockCollector("data")

        ctx.registry.register_collector("id1", collector1)
        ctx.registry.register_collector("id2", collector2)
        ctx.registry.register_collector("id3", collector3)

        executor.execute(ctx)

        self.assertTrue(collector1.called)
        self.assertFalse(collector2.called)
        self.assertTrue(collector3.called)


class ExecPlanExecutorTest(unittest.TestCase):

    def test_no_execution_done(self):
        ctx = test_context()
        ctx.flags.plan = True

        executor = ExecPlanExecutor()
        collector = MockCollector("data")
        validator = MockValidator(result=validation_result_with("data"))
        reactor_command = ReactorCommand(cmd=["do", "nothing"])
        reactor = MockReactor(reactor_command)

        ctx.registry.register_collector("id", collector)
        ctx.registry.register_validator("id", validator)
        ctx.registry.register_reactor("id", reactor)

        executor.execute(ctx)

        self.assertFalse(collector.called)
        self.assertFalse(validator.called)
        self.assertFalse(reactor.called)


def not_the_current_platform():
    if CURRENT_PLATFORM == Platform.MACOS:
        return Platform.LINUX
    else:
        return Platform.MACOS


class MockCollector(Collector):
    def __init__(self, result):
        self.result = result
        self.called = False

    def collect(self, ctx: Context) -> object:
        self.called = True
        return self.result


@target_platform(not_the_current_platform())
class PlatformInCompatible(MockCollector):
    def __init__(self):
        super().__init__("data")


@experimental
class ExperimentalMockCollector(MockCollector):
    def __init__(self):
        super().__init__("data")


@interactive
class InteractiveMockCollector(MockCollector):
    def __init__(self):
        super().__init__("data")


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


def validation_result_with(data, status: Status = Status.NOT_FOUND):
    return ValidationResult(data, status)


if __name__ == '__main__':
    unittest.main()
