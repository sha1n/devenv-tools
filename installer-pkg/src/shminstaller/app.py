from shminspector import embedded as inspector
from shminspector.clicontext import parse_context
from shminspector.api.executor import Executor
from shminspector.api.registry import Registry
from shminspector.components import *

from shminstaller.cliapp import CliAppRunner
from shminstaller.components.bazel import BazelInstallReactor
from shminstaller.components.brew import HomebrewInstallReactor
from shminstaller.components.docker import DockerInstallReactor
from shminstaller.components.gcloud import GCloudInstallReactor, GCloudConfigInstallReactor
from shminstaller.components.python import PythonInstallReactor, Python3InstallReactor
from shminstaller.components.xcode import XcodeInstallReactor


def register_components(registry: Registry):
    inspector.register_components(registry)

    registry.register_reactor(BREW_COMP_ID, HomebrewInstallReactor())
    registry.register_reactor(BAZEL_COMP_ID, BazelInstallReactor())
    registry.register_reactor(PYTHON_COMP_ID, PythonInstallReactor())
    registry.register_reactor(PYTHON3_COMP_ID, Python3InstallReactor())
    registry.register_reactor(XCODE_COMP_ID, XcodeInstallReactor())
    registry.register_reactor(GCLOUD_COMP_ID, GCloudInstallReactor())
    registry.register_reactor(GCLOUD_CONFIG_COMP_ID, GCloudConfigInstallReactor())
    registry.register_reactor(inspector.DOCKER_COMP_ID, DockerInstallReactor())

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
        if not ctx.flags.dryrun:
            ctx.logger.info("Inspecting components again to verify changes...")
            if inspector.run_embedded(_inspection_context()).problem_count > 0:
                ctx.logger.failure("Some issues could not be resolved. Please report this issue!")

    return execute()


def run():
    runner = CliAppRunner(name="installer",
                          description="Inspects your environment components and attempts to install or upgrade "
                                      "components that require changes",
                          register_components=register_components,
                          parse_context=parse_context,
                          run=run_embedded)
    return runner.run()
