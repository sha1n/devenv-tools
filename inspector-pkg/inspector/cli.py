import argparse

from inspector.api.context import Context
from inspector.api.context import Mode


def context(name):
    parser = argparse.ArgumentParser(description='Takes an environment dump for support purposes.')
    parser.add_argument("-m",
                        choices=["interactive", "debug", "background", "silent"],
                        dest="mode",
                        default="interactive",
                        help="one of [ interactive | background ]")

    args = parser.parse_args()

    return Context(name=name, mode=Mode.from_str(args.mode))


def run_safe(ctx: Context, fn):
    logger = ctx.logger
    logger.info("Running in {} mode".format(str(ctx.mode)))

    try:
        fn()

        logger.success("Done!")

    except Exception as err:
        logger.failure("Failure! %s" % err)
        exit(1)
