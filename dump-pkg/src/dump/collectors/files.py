import os
import shutil
import time
from shutil import copytree, copyfile

from inspector.util.error_handling import raised_to_none_wrapper


def copytree_if(source_dir, target_dir, modified_in_the_past_sec):
    copytree(
        src=source_dir,
        dst=target_dir,
        ignore=_ignore_files_mtime_gt(modified_in_the_past_sec)
    )


def try_copyfile(source_file, target_file, logger):
    raised_to_none_wrapper(copyfile, logger)(source_file, target_file)


def try_copytree(source_dir, target_dir, logger):
    raised_to_none_wrapper(copytree, logger)(source_dir, target_dir)


def try_copytree_if(source_dir, target_dir, modified_in_the_past_sec, logger):
    raised_to_none_wrapper(copytree_if, logger)(source_dir, target_dir, modified_in_the_past_sec)


def file_name_from(path):
    path_segments = os.path.split(path)
    return path_segments[len(path_segments) - 1]


# fixme shai: this method has the same naming convention as the try_copytree ones above, but behaves differently
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
