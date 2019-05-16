import oscmd
import console as log
from shutil import copyfile
from shutil import copytree
import os


def collect_intellij_info_files(user_home_dir_path, archive_dir_path):
    index = 0
    log.info("Collecting IntelliJ product(s) info...")
    for file_path in _collect_product_info_files():
        copyfile(file_path, "%s/intellij-product-info-%d.json" % (archive_dir_path, index))
        index += 1

    log.info("Collecting IntelliJ logs...")
    for logs_dir_path in _collect_log_libraries(user_home_dir_path):
        dir_name = _file_name_from(logs_dir_path)

        copytree(logs_dir_path, "%s/logs/%s" % (archive_dir_path, dir_name))

    log.info("Collecting IntelliJ user configuration files...")
    for config_dir_path in _collect_configurations(user_home_dir_path):
        dir_name = _file_name_from(config_dir_path)

        copytree(config_dir_path, "%s/configs/%s" % (archive_dir_path, dir_name))


def _collect_product_info_files():
    candidates = oscmd.cmd_output_for(["ls", "/Applications"]).split("\n")
    intellij_dirs = filter(lambda d: d.find("IntelliJ") == 0, candidates)

    return map(lambda d: "/Applications/" + d + "/Contents/Resources/product-info.json", intellij_dirs)


def _collect_log_libraries(user_home):
    candidates = oscmd.cmd_output_for(["ls", "%s/Library/Logs" % user_home]).split("\n")
    intellij_dirs = filter(lambda d: d.find("Idea") != -1, candidates)

    return map(lambda d: "%s/Library/Logs/%s" % (user_home, d), intellij_dirs)


def _collect_configurations(user_home):
    candidates = oscmd.cmd_output_for(["ls", "%s/Library/Preferences" % user_home]).split("\n")
    intellij_dirs = filter(lambda d: d.find("Idea") != -1, candidates)

    return map(lambda d: "%s/Library/Preferences/%s" % (user_home, d), intellij_dirs)


def _file_name_from(path):
    path_segments = os.path.split(path)
    return path_segments[len(path_segments) - 1]
