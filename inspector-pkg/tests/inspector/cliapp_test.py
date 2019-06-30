import unittest
import uuid

from inspector.api.context import Context, Mode
from inspector.api.semver import SemVer
from inspector.cliapp import CliAppRunner
from inspector.components.bazel import BazelInfo


class CliAppRunnerTest(unittest.TestCase):

    def test_contract(self):
        name = str(uuid.uuid4())
        comp_id = str(uuid.uuid4())
        probe = Probe(comp_id)

        # noinspection PyShadowingNames,PyUnusedLocal
        def parse_context(name, registry, description):
            return Context(name, registry, mode=Mode.BACKGROUND)

        runner = CliAppRunner(name, "",
                              register_components=probe.register_comps,
                              parse_context=parse_context,
                              run=probe.run)

        runner.run()

        self.assertEqual(name, probe.recorded_context.name)
        self.assertEqual(1, len(probe.recorded_registry.component_ids()))
        self.assertEqual(probe, probe.recorded_registry.find_collector(comp_id))
        self.assertEqual(probe.recorded_registry, probe.recorded_context.registry)
        self.assertGreater(probe.run_call_index, probe.register_comps_call_index)


def bazel_info_with(major="1", minor="24", patch="0", bazelisk=False):
    return BazelInfo(path="/", version=SemVer(major, minor, patch), bazelisk=bazelisk)


class Probe:
    def __init__(self, comp_id):
        self.comp_id = comp_id
        self.call_index = 0
        self.register_comps_call_index = -1
        self.run_call_index = -1
        self.recorded_context = None
        self.recorded_registry = None

    def register_comps(self, registry):
        self.recorded_registry = registry
        self.call_index += 1
        self.register_comps_call_index = self.call_index

        registry.register_collector(self.comp_id, self)

    def run(self, ctx):
        self.recorded_context = ctx
        self.call_index += 1
        self.run_call_index = self.call_index


if __name__ == '__main__':
    unittest.main()
