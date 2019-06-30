import platform
from enum import Enum

_TAGS_ATTR_NAME = "__tags_"


def tags(*values: str):
    return _set_tags((v for v in values))


def has_tag(obj, tag: str):
    _tags: set = getattr(obj, _TAGS_ATTR_NAME, set())
    return _tags.__contains__(tag)


def tags_of(obj):
    return getattr(obj, _TAGS_ATTR_NAME, set())


def _set_tags(values):
    def deco(c):
        _tags = tags_of(c)
        for v in values:
            _tags.add(v)

        setattr(c, _TAGS_ATTR_NAME, _tags)

        return c

    return deco


_EXPERIMENTAL_TAG_NAME = "@experimental"
_INTERACTIVE_TAG_NAME = "@interactive"


def experimental(cls):
    """
    A decorator designed to be used on component classes to mark them as experimental. Experimental features need to be
    enabled explicitly.
    """
    return tags(_EXPERIMENTAL_TAG_NAME)(cls)


def is_experimental(obj):
    return has_tag(obj, _EXPERIMENTAL_TAG_NAME)


def interactive(cls):
    """
    A decorator designed to be used on component classes to mark them as interactive. Components marked with this
    decorator, will only be executed in interactive mode.
    """
    return tags(_INTERACTIVE_TAG_NAME)(cls)


def is_interactive(obj):
    return has_tag(obj, _INTERACTIVE_TAG_NAME)


#
# Platform decorators
#

_PLATFORM_TAG_PREFIX = "@platform:"


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


def macos(cls):
    """
    A decorator to mark a component as MacOS specific
    """
    return tags(_platform_tag_name_for(Platform.MACOS))(cls)


def linux(cls):
    """
    A decorator to mark a component as Linux specific
    """
    return tags(_platform_tag_name_for(Platform.LINUX))(cls)


def target_platform(p: Platform):
    assert p != Platform.UNDEFINED, "UNDEFINED is not a valid platform"

    return tags(_platform_tag_name_for(p))


def _all_platform_tag(obj) -> set:
    return set((tag for tag in tags_of(obj) if tag.startswith(_PLATFORM_TAG_PREFIX)))


def is_compatible_with_current_platform(obj):
    platform_tags = _all_platform_tag(obj)

    return platform_tags.__len__() == 0 or platform_tags.__contains__(_platform_tag_name_for(CURRENT_PLATFORM))


def _platform_tag_name_for(p: Platform):
    return "{}{}".format(_PLATFORM_TAG_PREFIX, p.name.lower())


#
# Utilities
#
def stringify(obj):
    class_name = type(obj).__name__
    obj_tags = tags_of(obj)
    if len(obj_tags) > 0:
        tags_label = ", ".join(obj_tags)
        return "{class_name}[tags={tags}]".format(class_name=class_name, tags=tags_label)
    else:
        return class_name
