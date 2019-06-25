from inspector.api.executor import Executor
from inspector.api.registry import Registry
from inspector.api.semver import SemVer
from inspector.cliapp import CliAppRunner
from inspector.components.bazel import BazelInfoCollector, BazelInfoValidator
from inspector.components.brew import HomebrewCollector, HomebrewValidator
from inspector.components.debugreactor import DebugReactor
from inspector.components.disk import DiskInfoCollector, DiskInfoValidator
from inspector.components.hardware import HardwareInfoValidator, HardwareInfoCollector
from inspector.components.network import UrlConnectivityInfoCollector, UrlConnectivityInfoValidator
from inspector.components.python import PythonInfoCollector, PythonInfoValidator, PythonInfoStrictValidator
from inspector.components.xcode import XcodeInfoCollector, XcodeInfoValidator

HARDWARE_COMP_ID = "hardware config"
DISK_COMP_ID = "disk space"
NET_COMP_ID = "network connectivity"
BREW_COMP_ID = "homebrew"
BAZEL_COMP_ID = "bazel"
PYTHON_COMP_ID = "python"
PYTHON3_COMP_ID = "python3"
XCODE_COMP_ID = "xcode"


def register_components(registry: Registry):
    log_reactor = DebugReactor()

    registry.register_collector(NET_COMP_ID, UrlConnectivityInfoCollector())
    registry.register_validator(NET_COMP_ID, UrlConnectivityInfoValidator())
    registry.register_reactor(NET_COMP_ID, log_reactor)

    registry.register_collector(HARDWARE_COMP_ID, HardwareInfoCollector())
    registry.register_validator(HARDWARE_COMP_ID, HardwareInfoValidator())
    registry.register_reactor(HARDWARE_COMP_ID, log_reactor)

    registry.register_collector(DISK_COMP_ID, DiskInfoCollector())
    registry.register_validator(DISK_COMP_ID, DiskInfoValidator())
    registry.register_reactor(DISK_COMP_ID, log_reactor)

    registry.register_collector(BREW_COMP_ID, HomebrewCollector())
    registry.register_validator(BREW_COMP_ID, HomebrewValidator())
    registry.register_reactor(BREW_COMP_ID, log_reactor)

    registry.register_collector(XCODE_COMP_ID, XcodeInfoCollector())
    registry.register_validator(XCODE_COMP_ID, XcodeInfoValidator())
    registry.register_reactor(XCODE_COMP_ID, log_reactor)

    registry.register_collector(BAZEL_COMP_ID, BazelInfoCollector())
    registry.register_validator(BAZEL_COMP_ID, BazelInfoValidator())
    registry.register_reactor(BAZEL_COMP_ID, log_reactor)

    registry.register_collector(PYTHON_COMP_ID, PythonInfoCollector())
    registry.register_validator(PYTHON_COMP_ID, PythonInfoValidator(expected_ver=SemVer("2", "7", "0")))
    registry.register_reactor(PYTHON_COMP_ID, log_reactor)

    registry.register_collector(PYTHON3_COMP_ID, PythonInfoCollector(binary_name="python3"))
    registry.register_validator(PYTHON3_COMP_ID, PythonInfoStrictValidator(expected_ver=SemVer("3", "6", "8")))
    registry.register_reactor(PYTHON3_COMP_ID, log_reactor)


def run_embedded(ctx):
    executor = Executor()

    def execute():
        summary = executor.execute(ctx)

        if summary.problem_count == 0:
            ctx.logger.success("No problems detected!")

        return summary

    return execute()


def run():
    runner = CliAppRunner(name="inspector",
                          description="Inspects your environment components and prints out status messages in case "
                                      "issues are detected",
                          register_components=register_components,
                          run=run_embedded)

    issues_count = runner.run()

    return issues_count
