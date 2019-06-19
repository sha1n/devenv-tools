from inspector import app as inspector
from inspector.api.executor import Executor
from inspector.cli import run_safe, context
from installer.components.bazel import BazelInstallReactor
from installer.components.python import PythonInstallReactor
from installer.components.xcode import XcodeInstallReactor


def run():
    ctx = _installer_context()
    executor = Executor()

    def execute():
        ctx.logger.info("Starting the installer...")

        verify_changes(executor.execute(ctx))

        ctx.logger.info("Installer finished.")

    def verify_changes(summary):
        if summary.problem_count > 0:
            ctx.logger.info("Inspecting components again to verify changes...")
            if inspector.run_embedded(_inspection_context()).problem_count > 0:
                ctx.logger.failure("Some issues could not be resolved. Please report this issue!")
        else:
            ctx.logger.success("No problems detected!")

    run_safe(ctx, execute)


def _inspection_context():
    registry = inspector.create_component_registry()
    ctx = context("installer", registry)

    return ctx


def _installer_context():
    ctx = _inspection_context()
    registry = ctx.registry

    registry.register_reactor(inspector.BAZEL_COMP_ID, BazelInstallReactor())
    registry.register_reactor(inspector.PYTHON_COMP_ID, PythonInstallReactor())
    # registry.register_reactor(inspector.PYTHON3_COMP_ID, Python3InstallReactor())
    registry.register_reactor(inspector.XCODE_COMP_ID, XcodeInstallReactor())

    return ctx
