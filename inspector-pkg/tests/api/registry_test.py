import unittest

from inspector.api.platformcompatibility import Platform, CURRENT_PLATFORM, compatible_with
from inspector.api.registry import Registry


class RegistryTest(unittest.TestCase):

    def test_empty(self):
        registry = Registry()

        self.assertEqual(0, len(registry.component_ids()))

    def test_basic_registry(self):
        registry = Registry()
        comp_id = "test"

        implied_compatible = ImpliedCompatible()

        registry.register_collector(comp_id, implied_compatible)
        registry.register_validator(comp_id, implied_compatible)
        registry.register_reactor(comp_id, implied_compatible)

        self.assertEqual(implied_compatible, registry.find_collector(comp_id))
        self.assertEqual(implied_compatible, registry.find_validator(comp_id))
        self.assertEqual([implied_compatible], registry.find_reactors(comp_id))

    def test_compatible_registry(self):
        registry = Registry()
        comp_id = "test"

        annotated_compatible = PlatformCompatible()

        registry.register_collector(comp_id, annotated_compatible)
        registry.register_validator(comp_id, annotated_compatible)
        registry.register_reactor(comp_id, annotated_compatible)

        self.assertEqual(annotated_compatible, registry.find_collector(comp_id))
        self.assertEqual(annotated_compatible, registry.find_validator(comp_id))
        self.assertEqual([annotated_compatible], registry.find_reactors(comp_id))

    def test_incompatible_registry(self):
        registry = Registry()
        comp_id = "test"

        annotated_incompatible = PlatformInCompatible()

        registry.register_collector(comp_id, annotated_incompatible)
        registry.register_validator(comp_id, annotated_incompatible)
        registry.register_reactor(comp_id, annotated_incompatible)

        self.assertIsNone(registry.find_collector(comp_id))
        self.assertIsNone(registry.find_validator(comp_id))
        self.assertEqual([], registry.find_reactors(comp_id))


def not_the_current_platform():
    if CURRENT_PLATFORM == Platform.MACOS:
        return Platform.LINUX
    else:
        return Platform.MACOS


class ImpliedCompatible:
    def dummy(self): pass


@compatible_with(CURRENT_PLATFORM)
class PlatformCompatible:
    def dummy(self): pass


@compatible_with(not_the_current_platform())
class PlatformInCompatible:
    def dummy(self): pass


if __name__ == '__main__':
    unittest.main()
