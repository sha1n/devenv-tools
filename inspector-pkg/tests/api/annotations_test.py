import unittest

from inspector.api.annotations import Platform, CURRENT_PLATFORM, compatible_with, linux, experimental, \
    is_experimental, _TARGET_PLATFORM_ATTR_NAME


class PlatformDecoratorsTest(unittest.TestCase):

    def test_generic_decorator(self):
        obj = GenericPlatformCompatible()

        self.assertEqual(Platform.MACOS, obj.__getattribute__(_TARGET_PLATFORM_ATTR_NAME))

    def test_specific_decorator(self):
        obj = ExperimentalLinuxCompatible()

        self.assertEqual(Platform.LINUX, obj.__getattribute__(_TARGET_PLATFORM_ATTR_NAME))


class ExperimentalTest(unittest.TestCase):

    def test_undecorated(self):
        obj = GenericPlatformCompatible()

        self.assertFalse(is_experimental(obj))

    def test_experimental(self):
        obj = ExperimentalLinuxCompatible()

        self.assertTrue(is_experimental(obj))


def not_the_current_platform():
    if CURRENT_PLATFORM == Platform.MACOS:
        return Platform.LINUX
    else:
        return Platform.MACOS


@compatible_with(Platform.MACOS)
class GenericPlatformCompatible:
    def dummy(self): pass


@linux
@experimental
class ExperimentalLinuxCompatible:
    def dummy(self): pass


if __name__ == '__main__':
    unittest.main()
