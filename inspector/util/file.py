import os
import shutil
import console as log


def name_from(path):
    path_segments = os.path.split(path)
    return path_segments[len(path_segments) - 1]


def try_copy_file(file_path, target_dir_path, target_name_prefix=""):
    if os.path.exists(file_path):
        name = name_from(file_path)
        shutil.copyfile(file_path, "%s/%s%s" % (target_dir_path, target_name_prefix, name))
    else:
        log.warn("%s file expected but not found." % file_path)