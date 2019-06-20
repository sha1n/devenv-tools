import unittest

from inspector.api.platformcompatibility import Platform, CURRENT_PLATFORM, compatible_with, linux


class PlatformDecoratorsTest(unittest.TestCase):

    def test_generic_decorator(self):
        obj = GenericPlatformCompatible()

        self.assertEqual(Platform.MACOS, obj.target_platform)

    def test_specific_decorator(self):
        obj = LinuxCompatible()

        self.assertEqual(Platform.LINUX, obj.target_platform)


def not_the_current_platform():
    if CURRENT_PLATFORM == Platform.MACOS:
        return Platform.LINUX
    else:
        return Platform.MACOS


@compatible_with(Platform.MACOS)
class GenericPlatformCompatible:
    def dummy(self): pass


@linux
class LinuxCompatible:
    def dummy(self): pass


if __name__ == '__main__':
    unittest.main()
