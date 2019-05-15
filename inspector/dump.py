#!/bin/python

import json
import os
import tempfile
from datetime import datetime
from shutil import copyfile
from shutil import copytree
import util.env as env
import util.intellij as intellij
import util.console as log

user_home_dir = os.path.expanduser("~")
tar_file_path = user_home_dir + ("/Desktop/envdump-%s.tar.gz" % datetime.now().isoformat())
archive_dir_path = tempfile.mkdtemp(prefix="envdmp-")


def prepare_env_info_file():
    info = env.snapshot()

    info_file_path = archive_dir_path + "/platform-info.json"

    with open(info_file_path, 'w') as json_file:
        json.dump(obj=info, fp=json_file, indent=2)


def prepare_intellij_info_files():
    index = 0
    for file_path in intellij.collect_product_info_files():
        copyfile(file_path, "%s/intellij-product-info-%d.json" % (archive_dir_path, index))
        index += 1

    for logs_dir_path in intellij.collect_log_libraries(user_home_dir):
        dir_name = _file_name_from(logs_dir_path)

        copytree(logs_dir_path, "%s/logs/%s" % (archive_dir_path, dir_name))


def create_dump_archive():
    os.system("tar -czf %s -C %s ." % (tar_file_path, archive_dir_path))


def _file_name_from(path):
    path_segs = os.path.split(path)
    return path_segs[len(path_segs) - 1]

log.info("Collecting platform info...")
prepare_env_info_file()
log.info("Collecting IntelliJ product(s) info...")
prepare_intellij_info_files()
log.warn("Preparing tar archive...")
create_dump_archive()
log.success("Done!")

os.system("open -R %s" % tar_file_path)
