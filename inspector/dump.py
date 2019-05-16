#!/bin/python

import os
import tempfile
from datetime import datetime

import util.console as log
import util.env as env
import util.intellij as intellij

user_home_dir_path = os.path.expanduser("~")
tar_file_path = user_home_dir_path + ("/Desktop/envdump-%s.tar.gz" % datetime.now().isoformat())
archive_dir_path = tempfile.mkdtemp(prefix="envdmp-")


def _prepare_env_info_file():
    log.info("Collecting platform info...")
    env.create_snapshot_file(archive_dir_path)


def _prepare_intellij_info_files():
    intellij.collect_intellij_info_files(user_home_dir_path, archive_dir_path)


def _create_dump_archive():
    log.info("Preparing tar archive...")
    os.system("tar -czf %s -C %s ." % (tar_file_path, archive_dir_path))


def _check_prerequisites():
    pass


def _safe(*methods):
    count = len(methods)

    for method in methods:
        try:
            method()
        except Exception as error:
            count -= 1
            log.error(error.message)

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
    log.failure(e.message)
    exit(1)

