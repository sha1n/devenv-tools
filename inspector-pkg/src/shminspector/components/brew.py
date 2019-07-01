from shminspector.api.tags import macos
from shminspector.components.command import command_collector, command_validator


@macos
@command_collector("brew")
@command_validator("brew")
class HomebrewCommandCollectorValidator:
    pass
