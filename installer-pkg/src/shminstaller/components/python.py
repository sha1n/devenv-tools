from shminspector.api.context import Context
from shminspector.api.reactor import Reactor, ReactorCommand
from shminspector.api.tags import macos, experimental, interactive, prerequisites
from shminspector.api.validator import ValidationResult, Status
from shminstaller.components.macosutil import download_and_install_commands_for


@macos
@experimental
@interactive
@prerequisites("disk-space", "network-connectivity")
class Python3InstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):

        commands = []
        if data.status == Status.NOT_FOUND:
            commands = download_and_install_commands_for(ctx.config["installer"]["python"]["macos_package_url"])
        else:
            ctx.logger.info("Python 3 already installed! Detected version: {} - {}!"
                            .format(data.input_data.version, data.status.name))

        return commands


@macos
@prerequisites("homebrew")
class PythonInstallReactor(Reactor):
    def __init__(self, formula="python2"):
        self.formula = formula

    def react(self, data: ValidationResult, ctx: Context):
        ctx.logger.info("Python already installed! Detected version: {} - {}!"
                        .format(data.input_data.version, data.status.name))

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
