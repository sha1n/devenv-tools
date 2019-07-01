from shminspector.api.context import Context
from shminspector.api.reactor import Reactor, ReactorCommand
from shminspector.api.tags import macos, interactive, prerequisites
from shminspector.api.validator import ValidationResult, Status
from shminstaller.components.macosutil import download_command_for


@macos
@interactive
@prerequisites("disk-space", "network-connectivity")
class HomebrewInstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):

        commands = []
        if data.status == Status.NOT_FOUND:
            download_command, file_path = download_command_for(
                "https://raw.githubusercontent.com/Homebrew/install/master/install")

            commands.append(download_command)
            commands.append(ReactorCommand(cmd=["ruby", "--", file_path]))
        else:
            ctx.logger.info("Homebrew already installed")

        return commands
