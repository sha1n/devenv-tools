from shminspector.api.executor import Executor
from shminspector.api.registry import Registry
from shminspector.api.semver import SemVer
from shminspector.components import *
from shminspector.components.bazel import BazelInfoCollector, BazelInfoValidator
from shminspector.components.brew import HomebrewCommandCollectorValidator
from shminspector.components.debugreactor import DebugReactor
from shminspector.components.disk import DiskInfoCollector, DiskInfoValidator
from shminspector.components.gcloud import GCloudCommandCollectorValidator, GCloudConfigCollector, \
    GCloudConfigValidator
from shminspector.components.hardware import HardwareInfoValidator, HardwareInfoCollector
from shminspector.components.network import UrlConnectivityInfoCollector, UrlConnectivityInfoValidator
from shminspector.components.python import PythonInfoCollector, PythonInfoValidator, PythonInfoStrictValidator
from shminspector.components.xcode import XcodeInfoCollector, XcodeInfoValidator


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

    registry.register_collector(BREW_COMP_ID, HomebrewCommandCollectorValidator())
    registry.register_validator(BREW_COMP_ID, HomebrewCommandCollectorValidator())
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

    registry.register_collector(GCLOUD_COMP_ID, GCloudCommandCollectorValidator())
    registry.register_validator(GCLOUD_COMP_ID, GCloudCommandCollectorValidator())
    registry.register_reactor(GCLOUD_COMP_ID, log_reactor)

    registry.register_collector(GCLOUD_CONFIG_COMP_ID, GCloudConfigCollector())
    registry.register_validator(GCLOUD_CONFIG_COMP_ID, GCloudConfigValidator())
    registry.register_reactor(GCLOUD_CONFIG_COMP_ID, log_reactor)


def run_embedded(ctx):
    executor = Executor()

    def execute():
        summary = executor.execute(ctx)

        if summary.problem_count == 0:
            ctx.logger.success("No problems detected!")

        return summary

    return execute()


