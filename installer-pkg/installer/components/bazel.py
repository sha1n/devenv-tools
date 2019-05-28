from inspector.api.context import Context
from inspector.api.reactor import Reactor, ReactorCommand
from inspector.api.validator import ValidationResult, Status


class BazelInstallReactor(Reactor):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def react(self, data: ValidationResult):
        commands = []

        if data.status == Status.OK:
            self.logger.info("Bazelisk installation detected. (will attempt upgrade).")
            commands.append(self._upgrade_bazelisk_command())

        elif data.status == Status.NOT_FOUND:
            self.logger.info("Bazel/Bazelisk installation not found. (will be installed).")
            commands += self._install_bazelisk_commands()

        else: # fixme shai: should probably be more explicit/strict
            self.logger.info("Bazel installation detected. (will be replaced by Bazelisk).")
            commands.append(self._uninstall_bazel_command())
            commands += self._install_bazelisk_commands()

        return commands

    @staticmethod
    def _install_bazelisk_commands():
        return [
            ReactorCommand(["brew", "tap", "bazelbuild/tap/bazelisk"], silent=True),
            ReactorCommand(["brew", "tap-pin", "bazelbuild/tap/bazelisk"], silent=True),
            ReactorCommand(["brew", "install", "bazelbuild/tap/bazelisk"])
        ]

    @staticmethod
    def _upgrade_bazelisk_command() -> ReactorCommand:
        return ReactorCommand(["brew", "upgrade", "bazelbuild/tap/bazelisk"], silent=True)

    @staticmethod
    def _uninstall_bazel_command():
        return ReactorCommand(["brew", "uninstall", "bazelbuild/tap/bazel"])
