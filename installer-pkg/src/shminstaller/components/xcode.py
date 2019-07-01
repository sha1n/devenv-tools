from shminspector.api.context import Context
from shminspector.api.reactor import Reactor, ReactorCommand
from shminspector.api.tags import macos, interactive, prerequisites
from shminspector.api.validator import ValidationResult, Status


@macos
@interactive
@prerequisites("disk-space", "network-connectivity")
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
