from inspector.api.context import Context
from inspector.api.reactor import Reactor, ReactorCommand
from inspector.api.tags import macos, interactive
from inspector.api.validator import ValidationResult, Status


@macos
@interactive
class XcodeInstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):
        commands = []

        if data.status == Status.NOT_FOUND:
            ctx.logger.info("Xcode CLI tools could not be detected! Will start interactive installer.")
            ctx.logger.warn("""IMPORTANT!
- If you recently changed/removed Xcode, it is recommended that you restart your machine after the installer 
  is done, unless you know exactly which programs need to be restarted.
- If Bazel complains about your Xcode path, please run `bazel clean --expunge` on the corresponding workspace.""")
            commands.append(ReactorCommand(["xcode-select", "--install"]))

        elif data.status == Status.OK:
            ctx.logger.info("Xcode Command Line Tools already installed")

        return commands
