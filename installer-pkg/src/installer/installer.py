from inspector import inspector
from inspector.api.executor import Executor
from inspector.cli import run_safe, context
from installer.components.bazel import BazelInstallReactor
from installer.components.python import PythonInstallReactor


def install():
    ctx = _installer_context()
    executor = Executor()

    def execute():
        ctx.logger.info("Starting the installer...")

        executor.execute(ctx)

        ctx.logger.info("Installer finished.")

    run_safe(ctx, execute)


def _installer_context():
    registry = inspector.create_component_registry()
    ctx = context("installer", registry)

    registry.register_reactor(inspector.BAZEL_COMP_ID, BazelInstallReactor())

    registry.register_reactor(inspector.PYTHON_COMP_ID, PythonInstallReactor())

    return ctx
