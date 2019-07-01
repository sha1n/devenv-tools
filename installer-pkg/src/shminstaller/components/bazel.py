from shminspector.api.context import Context
from shminspector.api.reactor import Reactor, ReactorCommand
from shminspector.api.tags import macos, experimental, prerequisites
from shminspector.api.validator import ValidationResult, Status


@macos
@experimental
@prerequisites("homebrew")
class BazelInstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):
        commands = []

        if data.status == Status.OK:
            ctx.logger.info("Bazelisk installation detected. (will attempt upgrade).")
            commands.append(self._upgrade_bazelisk_command())

        elif data.status == Status.NOT_FOUND:
            ctx.logger.info("Bazel/Bazelisk installation not found. (will be installed).")
            commands += self._install_bazelisk_commands()

        else:  # fixme shai: should probably be more explicit/strict
            ctx.logger.info("Bazel installation detected. (will be replaced by Bazelisk).")
            commands.append(self._uninstall_bazel_command())
            commands += self._install_bazelisk_commands()

        return commands

    @staticmethod
    def _install_bazelisk_commands():
        return [
            ReactorCommand(["brew", "tap", "bazelbuild/tap"], silent=True),
            ReactorCommand(["brew", "tap-pin", "bazelbuild/tap"], silent=True),
            ReactorCommand(["brew", "install", "bazelbuild/tap/bazelisk"])
        ]

    @staticmethod
    def _upgrade_bazelisk_command() -> ReactorCommand:
        return ReactorCommand(["brew", "upgrade", "bazelbuild/tap/bazelisk"], silent=True)

    @staticmethod
    def _uninstall_bazel_command():
        return ReactorCommand(["brew", "uninstall", "bazelbuild/tap/bazel"])
