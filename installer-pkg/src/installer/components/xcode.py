from inspector.api.context import Context, Mode
from inspector.api.annotations import macos
from inspector.api.reactor import Reactor, ReactorCommand
from inspector.api.validator import ValidationResult, Status


@macos
class XcodeInstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):
        commands = []

        if data.status == Status.NOT_FOUND:
            self.interactive_installer(commands, ctx)

        elif data.status == Status.OK:
            ctx.logger.info("Xcode CLI Tools installed")

        return commands

    def interactive_installer(self, commands, ctx):
        if ctx.mode.value <= Mode.INTERACTIVE.value:
            ctx.logger.info("Xcode CLI tools could not be detected! Will start interactive installer.")
            ctx.logger.warn(
                """IMPORTANT!
    - If you recently changed/removed Xcode, it is recommended that you restart your machine after the installer 
      is done, unless you know exactly which programs need to be restarted.
    - If Bazel complains about your Xcode path, please run `bazel clean --expunge` on the corresponding workspace.""")

            commands.append(ReactorCommand(["xcode-select", "--install"]))
        else:
            ctx.logger.warn("Xcode CLI tools cannot be installed in non-interactive mode.")
            ctx.logger.warn("Please run the installer again in interactive mode.")
