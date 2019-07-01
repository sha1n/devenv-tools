import unittest

from shminspector.api.registry import Registry


class RegistryTest(unittest.TestCase):

    def test_empty(self):
        registry = Registry()

        self.assertEqual(0, len(registry.component_ids()))

    def test_basic_registry(self):
        registry = Registry()
        comp_id = "test"

        implied_compatible = DummyHandler()

        registry.register_collector(comp_id, implied_compatible)
        registry.register_validator(comp_id, implied_compatible)
        registry.register_reactor(comp_id, implied_compatible)

        self.assertEqual(implied_compatible, registry.find_collector(comp_id))
        self.assertEqual(implied_compatible, registry.find_validator(comp_id))
        self.assertEqual([implied_compatible], registry.find_reactors(comp_id))


class DummyHandler:
    def dummy(self): pass


if __name__ == '__main__':
    unittest.main()
