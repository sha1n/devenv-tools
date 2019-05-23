from typing import Generator

from inspector.reactors.basereactor import Reactor, ReactorCommand
from inspector.validators.basevalidator import ValidationResult, Status
from inspector.commons.context import Context


class BazelValidationLogReactor(Reactor):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def react(self, data: ValidationResult) -> Generator[ReactorCommand, None, None]:
        if data.status != Status.OK:
            self.logger.warn("Incompatible Bazel version: {}".format(str(data.input_data.version)))

        return
        yield


class BazelValidationInstallReactor(Reactor):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def react(self, data: ValidationResult):
        if data.status == Status.NOT_FOUND:
            yield self._install()
        elif data.status == data.status.UPGRADE_REQUIRED:
            yield self._upgrade()
        elif data.status == data.status.DOWNGRADE_REQUIRED:
            yield self._uninstall()
            yield self._install()

    # fixme that command is not necessarily the real one
    @staticmethod
    def _install() -> ReactorCommand: return ReactorCommand(["brew", "install", "bazel"])

    # fixme that command is not necessarily the real one
    @staticmethod
    def _upgrade() -> ReactorCommand: return ReactorCommand(["brew", "upgrade", "bazel"])

    # fixme that command is not necessarily the real one
    @staticmethod
    def _uninstall() -> ReactorCommand: return ReactorCommand(["brew", "uninstall", "bazel"])
