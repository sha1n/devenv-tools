import argparse
import getpass
import os
import platform
import tarfile
import tempfile
from datetime import datetime

from dump.collectors.env import EnvDataCollector
from dump.collectors.jetbrains import JetBrainsProductDataCollector, JetBrainsProductInfo
from inspector.api.context import Context
from inspector.api.registry import Registry
from inspector.cliapp import run_safe

platform.uname()
user_home_dir_path = os.path.expanduser("~")
default_target_dir_path = user_home_dir_path + "/tmp/env_dumps"
username = getpass.getuser()
archive_content_dir_path = tempfile.mkdtemp(prefix="envdmp-{}-".format(username))


def _prepare_env_info_file(ctx):
    env_info_target_dir_path = "{}/env".format(archive_content_dir_path)
    os.mkdir(env_info_target_dir_path)

    env = EnvDataCollector(ctx, user_home_dir_path, env_info_target_dir_path)
    env.collect()


def _prepare_intellij_info_files(ctx):
    intellij_target_dir_path = "%s/intellij" % archive_content_dir_path

    intellij = JetBrainsProductDataCollector(
        product_info=JetBrainsProductInfo(name="IntelliJ", log_dir_segment="Idea", pref_dir_segment="Idea"),
        user_home_dir_path=user_home_dir_path,
        target_dir_path=intellij_target_dir_path,
        ctx=ctx
    )
    intellij.collect()


def _prepare_goland_info_files(ctx):
    goland_target_dir_path = "{}/goland".format(archive_content_dir_path)

    goland = JetBrainsProductDataCollector(
        product_info=JetBrainsProductInfo(name="GoLand", log_dir_segment="GoLand", pref_dir_segment="GoLand"),
        user_home_dir_path=user_home_dir_path,
        target_dir_path=goland_target_dir_path,
        ctx=ctx
    )

    goland.collect()


def _prepare_pycharm_info_files(ctx):
    pycharm_target_dir_path = "{}/pycharm".format(archive_content_dir_path)

    pycharm = JetBrainsProductDataCollector(
        product_info=JetBrainsProductInfo(name="PyCharm", log_dir_segment="PyCharm", pref_dir_segment="PyCharm"),
        user_home_dir_path=user_home_dir_path,
        target_dir_path=pycharm_target_dir_path,
        ctx=ctx
    )
    pycharm.collect()


def _create_dump_archive(ctx):
    ctx.logger.info("Preparing tar archive...")

    if ctx.log_file_path is not None and os.path.exists(ctx.log_file_path):
        os.system("cp {} {}".format(ctx.log_file_path, "{}/self.log".format(archive_content_dir_path)))

    with tarfile.open(ctx.flags.out_file, "w:gz") as tar:
        tar.add(archive_content_dir_path, arcname=os.path.basename(archive_content_dir_path))


def _check_prerequisites(ctx):
    ctx.logger.progress("Checking prerequisites...")
    os_name = platform.system()
    if os_name != "Darwin":
        raise Exception("Unsupported operating system '%s'" % os_name)


def _safe(ctx, *methods):
    count = len(methods)

    for method in methods:
        try:
            method(ctx)
        except Exception as err:
            count -= 1
            ctx.logger.error(err)

    if count == 0:
        raise Exception("All data collection tasks have failed...")


def tarball():
    ctx = _parse_context()  # fixme shai: use executor where possible

    def dump(context):
        _check_prerequisites(context)

        _safe(
            context,
            _prepare_env_info_file,
            _prepare_intellij_info_files,
            _prepare_goland_info_files,
            _prepare_pycharm_info_files,
        )
        if not ctx.flags.dryrun:
            _create_dump_archive(context)
            os.system("open -R %s" % ctx.flags.out_file)
        else:
            ctx.logger.info("Dry-run mode: archive creation skipped!")

    run_safe(ctx, dump)


def _parse_context():
    parser = argparse.ArgumentParser(description=
                                     "Collects environment information and packs it all into a tar archive for support "
                                     "purposes.")
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
    parser.add_argument("--output", "-o",
                        default=None,
                        dest="out_file",
                        help="absolute path to the output tar archive")

    args = parser.parse_args()

    context = Context(
        name="dump",
        config_file=args.config_file,
        registry=Registry(),
        debug=args.debug,
        log_file=args.log_file,
        experimental=args.experimental,
    )

    context.flags.out_file = resolve_output_file_path(args)

    return context


def resolve_output_file_path(args):
    if args.out_file is not None:
        return args.out_file
    else:
        os.makedirs(default_target_dir_path, exist_ok=True)
        return "{}/envdump-{}-{}.tar.gz".format(default_target_dir_path, username, datetime.now().isoformat())
