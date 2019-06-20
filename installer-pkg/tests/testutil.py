import os

from inspector.api.context import Context, Mode
from inspector.api.registry import Registry


def test_context(mode=None) -> Context:
    resolved_mode = mode
    if resolved_mode is None:
        resolved_mode = Mode.from_str(os.environ.get('INSPECTOR_TEST_MODE', str(Mode.BACKGROUND)))

    return Context(name="test", mode=resolved_mode, dryrun=True, registry=Registry())
