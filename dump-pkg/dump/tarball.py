#!/bin/python

import os
import platform
import tarfile
import tempfile
from datetime import datetime

from dump.collectors.env import EnvDataCollector
from dump.collectors.jetbrains import JetBrainsProductDataCollector, JetBrainsProductInfo
from inspector.cli import context, run_safe

user_home_dir_path = os.path.expanduser("~")
archive_target_dir_path = user_home_dir_path + "/Desktop/env_dumps"
tar_file_path = "%s/envdump-%s.tar.gz" % (archive_target_dir_path, datetime.now().isoformat())
archive_content_dir_path = tempfile.mkdtemp(prefix="envdmp-")


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

    os.makedirs(archive_target_dir_path, exist_ok=True)

    with tarfile.open(tar_file_path, "w:gz") as tar:
        tar.add(archive_content_dir_path, arcname=os.path.basename(archive_content_dir_path))


def _check_prerequisites(ctx):
    ctx.logger.log("Checking prerequisites...")
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
    ctx = context(name="dump")

    def dump():
        _check_prerequisites(ctx)

        _safe(
            ctx,
            _prepare_env_info_file,
            _prepare_intellij_info_files,
            _prepare_goland_info_files,
            _prepare_pycharm_info_files,
        )

        _create_dump_archive(ctx)
        os.system("open -R %s" % tar_file_path)

    run_safe(ctx, dump)
