from inspector.api.context import Context
from inspector.api.annotations import macos
from inspector.api.reactor import Reactor, ReactorCommand
from inspector.api.validator import ValidationResult, Status
from installer.components.macosutil import download_command_for


@macos
class HomebrewInstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):

        commands = []
        if data.status == Status.NOT_FOUND:
            download_command, file_path = download_command_for(
                "https://raw.githubusercontent.com/Homebrew/install/master/install")

            commands.append(download_command)
            commands.append(ReactorCommand(cmd=["ruby", "--", file_path]))
        else:
            ctx.logger.info("Homebrew installed")

        return commands
