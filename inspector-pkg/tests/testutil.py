import os
from inspector.api.context import Context, Mode
from inspector.api.registry import Registry


def test_context() -> Context:
    mode = Mode.from_str(os.environ.get('INSPECTOR_TEST_MODE', str(Mode.SILENT)))

    return Context(name="test", registry=Registry(), mode=mode, dryrun=True)
