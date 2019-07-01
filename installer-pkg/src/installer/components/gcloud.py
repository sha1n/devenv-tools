from inspector.api.context import Context
from inspector.api.reactor import Reactor, ReactorCommand, UserInput
from inspector.api.tags import macos, interactive, experimental, prerequisites
from inspector.api.validator import ValidationResult, Status


@macos
@interactive
@experimental
@prerequisites("homebrew")
class GCloudInstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):

        commands = []
        if data.status == Status.NOT_FOUND:
            commands.append(ReactorCommand(cmd=["brew", "cask", "install", "google-cloud-sdk"]))
        else:
            ctx.logger.info("Gcloud already installed")

        return commands


@macos
@interactive
@experimental
@prerequisites("gcloud", "network-connectivity")
class GCloudConfigInstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):

        commands = []
        if data.status == Status.NOT_FOUND:
            ctx.logger.info("Going to configure missing gcloud authentication...")

            if not data.input_data.docker_ok:
                commands.append(ReactorCommand(cmd=["gcloud", "auth", "configure-docker", "--quiet"]))

            if not data.input_data.auth_ok:
                email_input = UserInput(key="gcloud_email", prompt="\nPlease enter your GCloud email address: ")
                commands.append(ReactorCommand(cmd=["gcloud", "auth", "login", email_input]))
                commands.append(ReactorCommand(cmd=["gcloud", "auth", "application-default", "login"]))

        else:
            ctx.logger.info("Gcloud authentication already configured")

        return commands
