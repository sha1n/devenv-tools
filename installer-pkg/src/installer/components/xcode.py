from inspector.api.context import Context, Mode
from inspector.api.reactor import Reactor, ReactorCommand
from inspector.api.validator import ValidationResult, Status


class XcodeInstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):
        commands = []

        if data.status == Status.NOT_FOUND:
            self.interactive_installer(commands, ctx)

        elif data.status == Status.OK:
            ctx.logger.info("Xcode - OK!")

        return commands

    def interactive_installer(self, commands, ctx):
        if ctx.mode.value <= Mode.INTERACTIVE.value:
            ctx.logger.info("Xcode CLI tools could not be detected! Will start interactive installer.")
            commands.append(ReactorCommand(["xcode-select", "--install"]))
        else:
            ctx.logger.warn("Xcode CLI tools cannot be installed in non-interactive mode.")
            ctx.logger.warn("Please run the installer again in interactive mode.")
