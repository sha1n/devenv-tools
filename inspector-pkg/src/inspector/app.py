import argparse

from inspector.api.context import Context, Mode
from inspector.api.executor import Executor
from inspector.api.registry import Registry
from inspector.api.semver import SemVer
from inspector.cliapp import CliAppRunner
from inspector.components.bazel import BazelInfoCollector, BazelInfoValidator
from inspector.components.brew import HomebrewCommandCollectorValidator
from inspector.components.debugreactor import DebugReactor
from inspector.components.disk import DiskInfoCollector, DiskInfoValidator
from inspector.components.gcloud import GCloudCommandCollectorValidator, GCloudConfigCollector, \
    GCloudConfigValidator
from inspector.components.hardware import HardwareInfoValidator, HardwareInfoCollector
from inspector.components.network import UrlConnectivityInfoCollector, UrlConnectivityInfoValidator
from inspector.components.python import PythonInfoCollector, PythonInfoValidator, PythonInfoStrictValidator
from inspector.components.xcode import XcodeInfoCollector, XcodeInfoValidator

HARDWARE_COMP_ID = "hardware-config"
DISK_COMP_ID = "disk-space"
NET_COMP_ID = "network-connectivity"
BREW_COMP_ID = "homebrew"
BAZEL_COMP_ID = "bazel"
PYTHON_COMP_ID = "python"
PYTHON3_COMP_ID = "python3"
XCODE_COMP_ID = "xcode"
GCLOUD_COMP_ID = "gcloud"
GCLOUD_CONFIG_COMP_ID = "gcloud-config"


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


def run():
    runner = CliAppRunner(name="inspector",
                          description="Inspects your environment components and prints out status messages in case "
                                      "issues are detected",
                          register_components=register_components,
                          parse_context=parse_context,
                          run=run_embedded)

    issues_count = runner.run()

    return issues_count


def parse_context(name, registry: Registry, description=""):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--mode", "-m",
                        choices=["interactive", "background"],
                        dest="mode",
                        default="interactive",
                        help="one of [ interactive | background ]. "
                             "Note that some actions cannot be executed in non-interactive mode")
    parser.add_argument("--dry-run",
                        default=False,
                        dest="dryrun",
                        action="store_true",
                        help="runs in dry run mode. In that mode actions that modify your environment will not be "
                             "executed")
    parser.add_argument("--plan", "-p",
                        default=False,
                        dest="plan",
                        action="store_true",
                        help="prints out an execution plan (takes into account your platform and program flags)")
    parser.add_argument("--debug", "-d",
                        default=False,
                        dest="debug",
                        action="store_true",
                        help="logs debug information to the console")
    parser.add_argument("--experimental", "-e",
                        default=False,
                        dest="experimental",
                        action="store_true",
                        help="turns on experimental features")
    parser.add_argument("--log-file",
                        dest="log_file",
                        help="absolute path to optional log file")
    parser.add_argument("--config",
                        dest="config_file",
                        help="optional JSON config file path")
    parser.add_argument("--components",
                        default=None,
                        dest="components",
                        help="optional comma separated list of component names. Supported components are: {}"
                        .format(list(registry.component_ids())))

    args = parser.parse_args()

    if args.components is not None:
        components = (comp.strip() for comp in args.components.split(","))
    else:
        components = None

    return Context(
        name=name,
        config_file=args.config_file,
        registry=registry,
        mode=Mode.from_str(args.mode),
        debug=args.debug,
        log_file=args.log_file,
        plan=args.plan,
        dryrun=args.dryrun,
        experimental=args.experimental,
        components=components
    )
