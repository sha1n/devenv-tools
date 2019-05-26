import os
import shutil


def name_from(path):
    path_segments = os.path.split(path)
    return path_segments[len(path_segments) - 1]


def try_copy_file(file_path, target_dir_path, target_name_prefix):
    if os.path.exists(file_path):
        name = name_from(file_path)
        shutil.copyfile(file_path, "{}/{}{}".format(target_dir_path, target_name_prefix, name))
        return True
    else:
        return False
