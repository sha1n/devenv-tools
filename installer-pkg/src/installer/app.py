from inspector import app as inspector
from inspector.api.executor import Executor
from inspector.api.registry import Registry

from inspector.cliapp import CliAppRunner, parse_context
from installer.components.bazel import BazelInstallReactor
from installer.components.brew import HomebrewInstallReactor
from installer.components.gcloud import GCloudInstallReactor
from installer.components.python import PythonInstallReactor, Python3InstallReactor
from installer.components.xcode import XcodeInstallReactor


def register_components(registry: Registry):
    inspector.register_components(registry)

    registry.register_reactor(inspector.BREW_COMP_ID, HomebrewInstallReactor())
    registry.register_reactor(inspector.BAZEL_COMP_ID, BazelInstallReactor())
    registry.register_reactor(inspector.PYTHON_COMP_ID, PythonInstallReactor())
    registry.register_reactor(inspector.PYTHON3_COMP_ID, Python3InstallReactor())
    registry.register_reactor(inspector.XCODE_COMP_ID, XcodeInstallReactor())
    registry.register_reactor(inspector.GCLOUD_COMP_ID, GCloudInstallReactor())


def _inspection_context():
    registry = Registry()
    inspector.register_components(registry)
    ctx = parse_context(name="installer", registry=registry)

    return ctx


def run_embedded(ctx):
    executor = Executor()

    def execute():
        summary = executor.execute(ctx)

        if summary.problem_count > 0:
            verify_changes()
        else:
            ctx.logger.success("No problems detected!")

        return summary

    def verify_changes():
        ctx.logger.info("Inspecting components again to verify changes...")
        if inspector.run_embedded(_inspection_context()).problem_count > 0:
            ctx.logger.failure("Some issues could not be resolved. Please report this issue!")

    return execute()


def run():
    runner = CliAppRunner(name="installer",
                          description="Inspects your environment components and attempts to install or upgrade "
                                      "components that require changes",
                          register_components=register_components,
                          run=run_embedded)
    return runner.run()
