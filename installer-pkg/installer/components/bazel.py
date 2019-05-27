from inspector.api.context import Context
from inspector.api.reactor import Reactor, ReactorCommand
from inspector.api.validator import ValidationResult, Status


class BazelInstallReactor(Reactor):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def react(self, data: ValidationResult):
        self.ctx.logger.info("Detected Bazel version: {} - {}!".format(data.input_data.version, data.status.name))

        commands = []
        if data.status == Status.NOT_FOUND:
            commands.append(self._install_cmd())
        elif data.status == data.status.UPGRADE_REQUIRED:
            commands.append(self._upgrade_cmd())
        elif data.status == data.status.DOWNGRADE_REQUIRED:
            commands.append(self._uninstall_cmd())
            commands.append(self._install_cmd())

        return commands

    # fixme that command is not necessarily the real one
    @staticmethod
    def _install_cmd() -> ReactorCommand:
        return ReactorCommand(["brew", "install", "bazel"])

    # fixme that command is not necessarily the real one
    @staticmethod
    def _upgrade_cmd() -> ReactorCommand:
        return ReactorCommand(["brew", "upgrade", "bazel"])

    # fixme that command is not necessarily the real one
    @staticmethod
    def _uninstall_cmd() -> ReactorCommand:
        return ReactorCommand(["brew", "uninstall", "bazel"])
