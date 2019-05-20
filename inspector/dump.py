#!/bin/python

import os, platform, tempfile
from datetime import datetime

import util.console as log
import collectors.env as env
import collectors.intellij as intellij

user_home_dir_path = os.path.expanduser("~")
archive_target_dir_path = user_home_dir_path + "/Desktop/env_dumps"
tar_file_path = "%s/envdump-%s.tar.gz" % (archive_target_dir_path, datetime.now().isoformat())
archive_content_dir_path = tempfile.mkdtemp(prefix="envdmp-")


def _prepare_env_info_file():
    env_info_target_dir_path = "%s/env" % archive_content_dir_path
    os.mkdir(env_info_target_dir_path)

    user_home_bazel_files_dir_path = "%s/bazel" % env_info_target_dir_path
    os.mkdir(user_home_bazel_files_dir_path)

    user_home_d4m_files_dir_path = "%s/d4m" % env_info_target_dir_path
    os.mkdir(user_home_d4m_files_dir_path)

    env.create_snapshot_file(env_info_target_dir_path)
    env.copy_bazelrc_files(user_home_dir_path, user_home_bazel_files_dir_path)
    env.copy_docker4mac_files(user_home_dir_path, user_home_d4m_files_dir_path)


def _prepare_intellij_info_files():
    intellij_target_dir_path = "%s/intellij" % archive_content_dir_path
    os.mkdir(intellij_target_dir_path)

    intellij.collect_intellij_info_files(user_home_dir_path, intellij_target_dir_path)


def _create_dump_archive():
    log.info("Preparing tar archive...")
    if os.system("mkdir -p %s" % archive_target_dir_path) != 0:
        raise Exception("Failed to create dump target directory '%s'" % archive_target_dir_path)

    if os.system("tar -czf %s -C %s ." % (tar_file_path, archive_content_dir_path)) != 0:
        raise Exception("Failed to create dump archive '%s'" % tar_file_path)


def _check_prerequisites():
    os_name = platform.system()
    if os_name != "Darwin":
        raise Exception("Unsupported operating system \"%s\"" % os_name)


def _safe(*methods):
    count = len(methods)

    for method in methods:
        try:
            method()
        except Exception as err:
            count -= 1
            log.error(err)

    if count == 0:
        raise Exception("All data collection tasks have failed...")


try:

    _check_prerequisites()

    _safe(
        _prepare_env_info_file,
        _prepare_intellij_info_files,
        )

    _create_dump_archive()

    log.success("Done!")

    os.system("open -R %s" % tar_file_path)

except Exception as e:
    log.failure("Failure! %s" % e.message)
    exit(1)
