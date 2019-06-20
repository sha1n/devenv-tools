import platform
from enum import Enum


class Platform(Enum):
    MACOS = 1
    LINUX = 2
    UNDEFINED = 3


def current():
    system = platform.system()

    if system == "Darwin":
        return Platform.MACOS
    elif system == "Linux":
        return Platform.LINUX
    else:
        return Platform.UNDEFINED


CURRENT_PLATFORM = current()


def macos(cls):
    return compatible_with(p=Platform.MACOS)(cls)


def linux(cls):
    return compatible_with(p=Platform.LINUX)(cls)


def compatible_with(p: Platform):
    def deco(cls):
        setattr(cls, "target_platform", p)

        return cls

    return deco
