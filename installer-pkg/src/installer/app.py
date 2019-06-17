from inspector import app
from inspector.api.executor import Executor
from inspector.cli import run_safe, context
from installer.components.bazel import BazelInstallReactor
from installer.components.python import PythonInstallReactor
from installer.components.xcode import XcodeInstallReactor


def install():
    ctx = _installer_context()
    executor = Executor()

    def execute():
        ctx.logger.info("Starting the installer...")

        executor.execute(ctx)

        ctx.logger.info("Installer finished.")

    run_safe(ctx, execute)


def _installer_context():
    registry = app.create_component_registry()
    ctx = context("installer", registry)

    registry.register_reactor(app.BAZEL_COMP_ID, BazelInstallReactor())

    registry.register_reactor(app.PYTHON_COMP_ID, PythonInstallReactor())
    registry.register_reactor(app.PYTHON3_COMP_ID, PythonInstallReactor(formula="python3"))
    registry.register_reactor(app.XCODE_COMP_ID, XcodeInstallReactor())

    return ctx
