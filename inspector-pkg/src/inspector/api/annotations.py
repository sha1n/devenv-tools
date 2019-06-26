import platform
from enum import Enum


#
# Platform decorators
#

class Platform(Enum):
    MACOS = 1
    LINUX = 2
    UNDEFINED = 3


def _current_platform():
    system = platform.system()

    if system == "Darwin":
        return Platform.MACOS
    elif system == "Linux":
        return Platform.LINUX
    else:
        return Platform.UNDEFINED


CURRENT_PLATFORM = _current_platform()

_TARGET_PLATFORM_ATTR_NAME = "___target_platform_"


def macos(cls):
    """
    A decorator to mark a component as MacOS specific
    """
    return compatible_with(p=Platform.MACOS)(cls)


def linux(cls):
    """
    A decorator to mark a component as Linux specific
    """
    return compatible_with(p=Platform.LINUX)(cls)


def compatible_with(p: Platform):
    """
    A decorator designed to be used on component classes to mark them as platform specific.
    """

    def deco(cls):
        setattr(cls, _TARGET_PLATFORM_ATTR_NAME, p)

        return cls

    return deco


def is_compatible_with_current_platform(obj):
    target_platform = getattr(obj, _TARGET_PLATFORM_ATTR_NAME, Platform.UNDEFINED)
    return target_platform == Platform.UNDEFINED or target_platform == CURRENT_PLATFORM


#
# Generic flag decorator
#

def flag_with(name: str, value: bool):
    def deco(c):
        setattr(c, name, value)

        return c

    return deco


#
# experimental feature decorator.
#

_EXPERIMENTAL_ATTR_NAME = "___experimental_"


def experimental(cls):
    """
    A decorator designed to be used on component classes to mark them as experimental. Experimental features need to be
    enabled explicitly.
    """
    return flag_with(_EXPERIMENTAL_ATTR_NAME, True)(cls)


def is_experimental(obj):
    return hasattr(obj, _EXPERIMENTAL_ATTR_NAME) and obj.__getattribute__(_EXPERIMENTAL_ATTR_NAME) is True


#
# interactive feature decorator.
#

_INTERACTIVE_ATTR_NAME = "___interactive_"


def interactive(cls):
    """
    A decorator designed to be used on component classes to mark them as interactive. Components marked with this
    decorator, will only be executed in interactive mode.
    """
    return flag_with(_INTERACTIVE_ATTR_NAME, True)(cls)


def is_interactive(obj):
    return hasattr(obj, _INTERACTIVE_ATTR_NAME) and obj.__getattribute__(_INTERACTIVE_ATTR_NAME) is True


#
# Utilities
#
def stringify(obj):
    flags = []
    if is_experimental(obj):
        flags.append("experimental")

    if is_interactive(obj):
        flags.append("interactive")

    target_platform = getattr(obj, _TARGET_PLATFORM_ATTR_NAME, None)
    if target_platform is not None:
        flags.append(str(target_platform))

    class_name = type(obj).__name__
    if len(flags) > 0:
        return "{class_name}: {flags}".format(class_name=class_name, flags=flags)
    else:
        return class_name