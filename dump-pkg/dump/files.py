import os
import shutil
import time
from shutil import copytree


def copytree_if(source_dir, target_dir, modified_in_the_past_sec):
    copytree(
        src=source_dir,
        dst=target_dir,
        ignore=_ignore_files_mtime_gt(modified_in_the_past_sec)
    )


def file_name_from(path):
    path_segments = os.path.split(path)
    return path_segments[len(path_segments) - 1]


def try_copy_file(file_path, target_dir_path, target_name_prefix=""):
    if os.path.exists(file_path):
        name = file_name_from(file_path)
        shutil.copyfile(file_path, "{}/{}{}".format(target_dir_path, target_name_prefix, name))
        return True
    else:
        return False


def _ignore_files_mtime_gt(interval_sec):
    def ignore(path, names):
        return (name for name in names if os.path.getmtime("{}/{}".format(path, name)) < time.time() - interval_sec)

    return ignore
