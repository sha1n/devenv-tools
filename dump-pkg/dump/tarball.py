#!/bin/python

import os
import platform
import tarfile
import tempfile
from datetime import datetime

from dump.env import EnvDataCollector
from dump.jetbrains import JetBrainsProductDataCollector, JetBrainsProductInfo
from inspector.cli import context, run_safe

user_home_dir_path = os.path.expanduser("~")
archive_target_dir_path = user_home_dir_path + "/Desktop/env_dumps"
tar_file_path = "%s/envdump-%s.tar.gz" % (archive_target_dir_path, datetime.now().isoformat())
archive_content_dir_path = tempfile.mkdtemp(prefix="envdmp-")


def _prepare_env_info_file(ctx):
    env_info_target_dir_path = "%s/env" % archive_content_dir_path
    os.mkdir(env_info_target_dir_path)

    user_home_bazel_files_dir_path = "%s/bazel" % env_info_target_dir_path
    os.mkdir(user_home_bazel_files_dir_path)

    user_home_d4m_files_dir_path = "%s/docker" % env_info_target_dir_path
    os.mkdir(user_home_d4m_files_dir_path)

    env = EnvDataCollector(ctx)
    env.create_snapshot_file(env_info_target_dir_path)
    env.copy_bazelrc_files(user_home_dir_path, user_home_bazel_files_dir_path)
    env.copy_docker_config_files(user_home_dir_path, user_home_d4m_files_dir_path)


def _prepare_intellij_info_files(ctx):
    intellij_target_dir_path = "%s/intellij" % archive_content_dir_path

    intellij = JetBrainsProductDataCollector(
        JetBrainsProductInfo(name="IntelliJ", log_dir_segment="Idea", pref_dir_segment="Idea"), ctx)
    intellij.collect_info_files(user_home_dir_path, intellij_target_dir_path)


def _prepare_goland_info_files(ctx):
    goland_target_dir_path = "%s/goland" % archive_content_dir_path

    goland = JetBrainsProductDataCollector(
        JetBrainsProductInfo(name="GoLand", log_dir_segment="GoLand", pref_dir_segment="GoLand"), ctx)
    goland.collect_info_files(user_home_dir_path, goland_target_dir_path)


def _prepare_pycharm_info_files(ctx):
    pycharm_target_dir_path = "%s/pycharm" % archive_content_dir_path

    pycharm = JetBrainsProductDataCollector(
        JetBrainsProductInfo(name="PyCharm", log_dir_segment="PyCharm", pref_dir_segment="PyCharm"), ctx)
    pycharm.collect_info_files(user_home_dir_path, pycharm_target_dir_path)


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
