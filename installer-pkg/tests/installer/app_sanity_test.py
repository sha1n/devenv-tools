import unittest

from installer.app import run_embedded, _inspection_context
from tests.testutil import test_context


@unittest.skip  # argv passed by testing executing env screw the args parser
class InstallerSanityTestTest(unittest.TestCase):

    def test_dry_run_sanity(self):
        context = test_context()
        context.registry = _inspection_context().registry
        context.flags.dryrun = True

        summary = run_embedded(context)

        # just checking that something has been executed and that we got an expected result structure
        self.assertGreater(summary.total_count, 0)
        self.assertGreaterEqual(summary.problem_count, 0)


if __name__ == '__main__':
    unittest.main()
