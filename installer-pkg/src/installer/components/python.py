from inspector.api.context import Context
from inspector.api.reactor import Reactor, ReactorCommand
from inspector.api.validator import ValidationResult, Status


class PythonInstallReactor(Reactor):
    def __init__(self, formula="python"):
        self.formula = formula

    def react(self, data: ValidationResult, ctx: Context):
        ctx.logger.info("Detected Python version: {} - {}!".format(data.input_data.version, data.status.name))

        commands = []
        if data.status == Status.NOT_FOUND:
            commands.append(self._install_cmd())
        elif data.status == data.status.UPGRADE_REQUIRED:
            commands.append(self._upgrade_cmd())
        elif data.status == data.status.DOWNGRADE_REQUIRED:
            commands.append(self._uninstall_cmd())
            commands.append(self._install_cmd())

        return commands

    def _install_cmd(self) -> ReactorCommand:
        return ReactorCommand(["brew", "install", self.formula])

    def _upgrade_cmd(self) -> ReactorCommand:
        return ReactorCommand(["brew", "upgrade", self.formula])

    def _uninstall_cmd(self) -> ReactorCommand:
        return ReactorCommand(["brew", "uninstall", self.formula])
