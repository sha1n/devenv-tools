import json

from shminspector.api.context import Context
from shminspector.api.executor import ExecPlanExecutor
from shminspector.api.registry import Registry


class CliAppRunner:
    def __init__(self, name, description, register_components, parse_context, run):
        self.name = name
        self.description = description
        self._register_components = register_components
        self._do_run = run
        self.parse_context = parse_context

    def run(self):
        registry = Registry()
        self._register_components(registry)

        ctx = self.parse_context(name=self.name, registry=registry, description=self.description)

        ctx.logger.info("Starting {}.".format(self.name))
        _print_header(ctx)

        if ctx.flags.plan:
            _run_safe_execution_plan(ctx)
        else:
            run_safe(ctx, self._do_run)

        ctx.logger.info("{} finished.".format(self.name.capitalize()))


def _print_header(ctx):
    logger = ctx.logger

    if ctx.flags.plan:
        logger.info("Running in plan mode. No changes will be applied to the system.")
    elif ctx.flags.dryrun:
        logger.info("Running in dry-run mode. No changes will be applied to the system.")

    logger.debug("Execution context = {}".format(ctx))
    logger.debug("Configuration = {}".format(json.dumps(ctx.config, indent=2)))
    logger.debug("Running in {} mode".format(str(ctx.mode)))


def run_safe(ctx: Context, fn):
    try:
        fn(ctx)
    except Exception as err:
        ctx.logger.error(err)
        ctx.logger.failure("Unexpected error - exiting :(")
        exit(1)


def _run_safe_execution_plan(ctx: Context):
    run_safe(ctx, ExecPlanExecutor().execute)
