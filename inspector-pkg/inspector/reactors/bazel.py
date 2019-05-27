from inspector.api.context import Context
from inspector.api.reactor import Reactor, ReactorCommand
from inspector.api.validator import ValidationResult, Status


class BazelValidationLogReactor(Reactor):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def react(self, data: ValidationResult):
        if data.status != Status.OK:
            self.logger.warn("Incompatible Bazel version: {}".format(str(data.input_data.version)))

        return []


class BazelValidationInstallReactor(Reactor):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def react(self, data: ValidationResult):
        commands = []
        if data.status == Status.NOT_FOUND:
            commands.append(self._install())
        elif data.status == data.status.UPGRADE_REQUIRED:
            commands.append(self._upgrade())
        elif data.status == data.status.DOWNGRADE_REQUIRED:
            commands.append(self._uninstall())
            commands.append(self._install())

        return commands

    # fixme that command is not necessarily the real one
    @staticmethod
    def _install() -> ReactorCommand:
        return ReactorCommand(["brew", "install", "bazel"])

    # fixme that command is not necessarily the real one
    @staticmethod
    def _upgrade() -> ReactorCommand:
        return ReactorCommand(["brew", "upgrade", "bazel"])

    # fixme that command is not necessarily the real one
    @staticmethod
    def _uninstall() -> ReactorCommand:
        return ReactorCommand(["brew", "uninstall", "bazel"])
