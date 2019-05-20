from shutil import copyfile
from shutil import copytree
import os
import json
import time

from util import console as log
from util import cmd
from util import file

two_week_sec = 14 * 24 * 60 * 60  # days * hours * minutes * seconds


@log.timeit_if(more_than_sec=20)
def collect_intellij_info_files(user_home_dir_path, target_dir_path):
    log.info("Collecting IntelliJ product(s) info...")
    for file_path in _collect_product_info_files():
        version = _read_json_property(file_path, "version")
        code = _read_json_property(file_path, "productCode")
        copyfile(file_path, "%s/intellij-%s-%s-product-info.json" % (target_dir_path, code, version))

    log.info("\t- Collecting logs... (files older than two weeks will be ignored)")
    for logs_dir_path in _collect_log_libraries(user_home_dir_path):
        dir_name = file.name_from(logs_dir_path)

        copytree(
            src=logs_dir_path,
            dst="%s/logs/%s" % (target_dir_path, dir_name),
            ignore=_ignore_files_mtime_gt(two_week_sec)
        )

    log.info("\t- Collecting configuration files...")
    for config_dir_path in _collect_configurations(user_home_dir_path):
        dir_name = file.name_from(config_dir_path)

        copytree(config_dir_path, "%s/configs/%s" % (target_dir_path, dir_name))


@log.timeit_if(more_than_sec=3)
def _collect_product_info_files():
    candidates = cmd.execute(["ls", "/Applications"]).split("\n")
    intellij_dirs = filter(lambda d: d.find("IntelliJ") == 0, candidates)

    return map(lambda d: "/Applications/" + d + "/Contents/Resources/product-info.json", intellij_dirs)


@log.timeit_if(more_than_sec=10)
def _collect_log_libraries(user_home):
    candidates = cmd.execute(["ls", "%s/Library/Logs" % user_home]).split("\n")
    intellij_dirs = filter(lambda d: d.find("Idea") != -1, candidates)

    return map(lambda d: "%s/Library/Logs/%s" % (user_home, d), intellij_dirs)


def _collect_configurations(user_home):
    candidates = cmd.execute(["ls", "%s/Library/Preferences" % user_home]).split("\n")
    intellij_dirs = filter(lambda d: d.find("Idea") != -1, candidates)

    return map(lambda d: "%s/Library/Preferences/%s" % (user_home, d), intellij_dirs)


def _read_json_property(file_path, property_name):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data[property_name]


def _ignore_files_mtime_gt(interval_sec):
    def ignore(path, names):
        return filter(
            lambda name: os.path.getmtime("%s/%s" % (path, name)) < time.time() - interval_sec,
            names
        )

    return ignore
