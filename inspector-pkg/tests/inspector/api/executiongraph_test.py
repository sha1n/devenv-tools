import unittest

from shminspector.api.executor import ExecutionGraph, CyclicDependencyError, MissingDependencyError
from shminspector.api.tags import prerequisites
from tests.testutil import test_context


class ExecutionGraphTest(unittest.TestCase):

    def test_simple(self):
        context = test_context()
        context.registry.register_collector("c1", Comp1())
        context.registry.register_collector("c2", Comp2())
        context.registry.register_collector("c3", Comp3())
        context.registry.register_collector("c4", Comp4())

        nodes = list(ExecutionGraph(context).topologically_ordered_comp_ids())

        self.assertTrue(
            list(["c1", "c2", "c3", "c4"]) == nodes or list(["c2", "c1", "c3", "c4"]) == nodes
        )

    def test_direct_cycle(self):
        context = test_context()
        context.registry.register_collector("direct-cyc1", DirectCycle1())
        context.registry.register_collector("direct-cyc2", DirectCycle2())

        self.assertRaises(CyclicDependencyError, lambda *args: ExecutionGraph(context))

    def test_indirect_cycle(self):
        context = test_context()
        context.registry.register_collector("cyc1", Cycle1())
        context.registry.register_collector("cyc2", Cycle2())
        context.registry.register_collector("cyc3", Cycle3())

        self.assertRaises(CyclicDependencyError, lambda *args: ExecutionGraph(context))

    def test_missing_dep(self):
        context = test_context()
        context.registry.register_collector("c1", BrokenDep())

        self.assertRaises(MissingDependencyError, lambda *args: ExecutionGraph(context))


class Comp1:
    pass


class Comp2:
    pass


@prerequisites("c1", "c2")
class Comp3:
    pass


@prerequisites("c3", "c2")
class Comp4:
    pass


@prerequisites("cyc3")
class Cycle1:
    pass


@prerequisites("cyc1")
class Cycle2:
    pass


@prerequisites("cyc2")
class Cycle3:
    pass


@prerequisites("direct-cyc2")
class DirectCycle1:
    pass


@prerequisites("direct-cyc1")
class DirectCycle2:
    pass


@prerequisites("non-existing")
class BrokenDep:
    pass


if __name__ == '__main__':
    unittest.main()
