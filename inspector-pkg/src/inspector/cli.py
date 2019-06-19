import argparse

from inspector.api.context import Context
from inspector.api.context import Mode
from inspector.api.registry import Registry


def context(name, registry: Registry):
    parser = argparse.ArgumentParser(description='Takes an environment dump for support purposes.')
    parser.add_argument("-m",
                        choices=["interactive", "debug", "background", "silent"],
                        dest="mode",
                        default="interactive",
                        help="one of [ interactive | background ]")
    parser.add_argument("--dry-run",
                        default=False,
                        dest="dryrun",
                        action="store_true",
                        help="runs in dry run mode")

    args = parser.parse_args()

    return Context(name=name, registry=registry, mode=Mode.from_str(args.mode), dryrun=args.dryrun)


def run_safe(ctx: Context, fn):
    logger = ctx.logger
    if ctx.dryrun:
        logger.debug("*** DRY RUN ***")

    logger.progress("Running in {} mode".format(str(ctx.mode)))

    try:
        return fn()
    except Exception as err:
        logger.error(err)
        logger.failure("Unexpected error - exiting :(")
        exit(1)
