import unittest
from uuid import uuid4

from shminspector.api.tags import experimental, is_experimental, is_interactive, interactive, tags, has_tag, tags_of, \
    _platform_tag_name_for, Platform, CURRENT_PLATFORM, target_platform, linux, \
    is_compatible_with_current_platform, prerequisites, prerequisites_of

TAG_A = str(uuid4())
TAG_B = str(uuid4())
TAG_C = str(uuid4())
COMP_ID_A = str(uuid4())
COMP_ID_B = str(uuid4())


class TagsTest(unittest.TestCase):

    def test_tags_on_tagged_object(self):
        obj = TaggedDummy()

        self.assertTrue(has_tag(obj, TAG_A))
        self.assertTrue(has_tag(obj, TAG_B))
        self.assertFalse(has_tag(obj, TAG_C))

    def test_tags_on_untagged_object(self):
        obj = UnTaggedDummy()

        self.assertEqual(set(), tags_of(obj))

    def test_experimental_on_tagged_object(self):
        obj = TaggedDummy()

        self.assertTrue(is_experimental(obj))

    def test_experimental_on_untagged_object(self):
        obj = UnTaggedDummy()

        self.assertFalse(is_experimental(obj))

    def test_interactive_on_tagged_object(self):
        obj = TaggedDummy()

        self.assertTrue(is_interactive(obj))

    def test_interactive_on_untagged_object(self):
        obj = UnTaggedDummy()

        self.assertFalse(is_interactive(obj))

    def test_prerequisites_on_tagged_object(self):
        obj = TaggedDummy()

        self.assertEqual({COMP_ID_A, COMP_ID_B}, prerequisites_of(obj))

    def test_prerequisites_on_untagged_object(self):
        obj = UnTaggedDummy()

        self.assertEqual(set(), prerequisites_of(obj))


@tags(TAG_A, TAG_B)
@prerequisites(COMP_ID_A, COMP_ID_B)
@interactive
@experimental
class TaggedDummy:
    pass


class UnTaggedDummy:
    pass


class PlatformDecoratorsTest(unittest.TestCase):

    def test_generic_decorator(self):
        obj = GenericPlatformCompatible()

        self.assertTrue(has_tag(obj, _platform_tag_name_for(Platform.MACOS)))
        self.assertEqual(CURRENT_PLATFORM == Platform.MACOS, is_compatible_with_current_platform(obj))

    def test_specific_decorator(self):
        obj = LinuxCompatible()

        self.assertTrue(has_tag(obj, _platform_tag_name_for(Platform.LINUX)))
        self.assertEqual(CURRENT_PLATFORM == Platform.LINUX, is_compatible_with_current_platform(obj))

    def test_untagged(self):
        obj = UnTaggedDummy()

        self.assertTrue(is_compatible_with_current_platform(obj))


def not_the_current_platform():
    if CURRENT_PLATFORM == Platform.MACOS:
        return Platform.LINUX
    else:
        return Platform.MACOS


@target_platform(Platform.MACOS)
class GenericPlatformCompatible:
    pass


@linux
class LinuxCompatible:
    pass


if __name__ == '__main__':
    unittest.main()
