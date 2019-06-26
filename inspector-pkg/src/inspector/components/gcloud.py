from inspector.api.annotations import macos
from inspector.components.command import command_collector, command_validator


@macos
@command_collector("gcloud")
@command_validator("gcloud")
class GCloudCommandCollectorValidator:
    pass
