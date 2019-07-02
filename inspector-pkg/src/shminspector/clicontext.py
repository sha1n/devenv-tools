import argparse

from shminspector.api.context import Context, Mode
from shminspector.api.registry import Registry


def parse_context(name, registry: Registry, description=""):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--mode", "-m",
                        choices=["interactive", "background"],
                        dest="mode",
                        default="interactive",
                        help="one of [ interactive | background ]. "
                             "Note that some actions cannot be executed in non-interactive mode")
    parser.add_argument("--dry-run",
                        default=False,
                        dest="dryrun",
                        action="store_true",
                        help="runs in dry run mode. In that mode actions that modify your environment will not be "
                             "executed")
    parser.add_argument("--plan", "-p",
                        default=False,
                        dest="plan",
                        action="store_true",
                        help="prints out an execution plan (takes into account your platform and program flags)")
    parser.add_argument("--debug", "-d",
                        default=False,
                        dest="debug",
                        action="store_true",
                        help="logs debug information to the console")
    parser.add_argument("--experimental", "-e",
                        default=False,
                        dest="experimental",
                        action="store_true",
                        help="turns on experimental features")
    parser.add_argument("--log-file",
                        dest="log_file",
                        help="absolute path to optional log file")
    parser.add_argument("--config",
                        dest="config_file",
                        help="optional JSON config file path")
    parser.add_argument("--components",
                        default=None,
                        dest="components",
                        help="optional comma separated list of component names. Supported components are: {}"
                        .format(list(registry.component_ids())))

    args = parser.parse_args()

    if args.components is not None:
        components = [comp.strip() for comp in args.components.split(",")]
    else:
        components = None

    return Context(
        name=name,
        config_file=args.config_file,
        registry=registry,
        mode=Mode.from_str(args.mode),
        debug=args.debug,
        log_file=args.log_file,
        plan=args.plan,
        dryrun=args.dryrun,
        experimental=args.experimental,
        components=components
    )
