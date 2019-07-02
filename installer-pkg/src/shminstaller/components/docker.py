from shminspector.api.context import Context
from shminspector.api.reactor import Reactor, ReactorCommand
from shminspector.api.tags import macos, experimental, interactive, prerequisites
from shminspector.api.validator import ValidationResult, Status
from shminstaller.components.macosutil import download_command_for, mount_command_for


@macos
@experimental
@interactive
@prerequisites("disk-space", "network-connectivity")
class DockerInstallReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):

        commands = []
        if data.status == Status.NOT_FOUND:
            download_command, dmg_file = download_command_for(ctx.config["installer"]["docker"]["macos_package_url"])
            commands.append(download_command)
            commands.append(mount_command_for(dmg_file))
            commands.append(ReactorCommand(["cp", "-r", "/Volumes/Docker/Docker.app", "/Applications"]))
        elif data.status == Status.OK:
            ctx.logger.info("Docker already installed!")

        return commands
