import os
import time
from shutil import copytree, copyfile

from inspector.util.error_handling import raised_to_none_wrapper
from inspector.util.logger import NOOP_LOGGER


def mkdir(path):
    os.mkdir(path)


def path_exists(path):
    return os.path.exists(path)


def file_path(path, *paths):
    return os.path.join(path, *paths)


def copytree_if(source_dir, target_dir, modified_in_the_past_sec):
    copytree(
        src=source_dir,
        dst=target_dir,
        ignore=_ignore_files_mtime_gt(modified_in_the_past_sec)
    )


def try_copyfile(source_file, target_file, logger=NOOP_LOGGER):
    raised_to_none_wrapper(copyfile, logger)(source_file, target_file)


def try_copytree(source_dir, target_dir, logger=NOOP_LOGGER):
    raised_to_none_wrapper(copytree, logger)(source_dir, target_dir)


def try_copytree_if(source_dir, target_dir, modified_in_the_past_sec, logger=NOOP_LOGGER):
    raised_to_none_wrapper(copytree_if, logger)(source_dir, target_dir, modified_in_the_past_sec)


def file_name_from(path):
    path_segments = os.path.split(path)
    return path_segments[len(path_segments) - 1]


def _ignore_files_mtime_gt(interval_sec):
    def ignore(path, names):
        return (name for name in names if os.path.getmtime("{}/{}".format(path, name)) < time.time() - interval_sec)

    return ignore
