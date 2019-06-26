from inspector.api.annotations import macos, interactive, experimental
from inspector.api.context import Context
from inspector.api.reactor import Reactor, ReactorCommand
from inspector.api.validator import ValidationResult, Status


@macos
@interactive
@experimental
class GCloudInstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):

        commands = []
        if data.status == Status.NOT_FOUND:
            email = input("Please enter your Google Cloud account email address: ")

            commands.append(ReactorCommand(cmd=["brew", "cask", "install", "google-cloud-sdk"]))
            commands.append(ReactorCommand(cmd=["gcloud", "auth", "configure-docker"]))
            commands.append(ReactorCommand(cmd=["gcloud", "auth", "login", email]))
            commands.append(ReactorCommand(cmd=["gcloud", "auth", "application-default", "login"]))

        else:
            ctx.logger.info("Gcloud installed")

        return commands
