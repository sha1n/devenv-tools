import getpass
import multiprocessing
import subprocess
import json
import platform
from datetime import datetime
import shutil
from os import path

from util import console as log
from util import oscmd as oscmd


@log.timeit_if(more_than_sec=5)
def create_snapshot_file(target_dir_path):
    log.info("Collecting platform info...")

    data = snapshot()

    info_file_path = target_dir_path + "/platform-data.json"

    with open(info_file_path, 'w') as json_file:
        json.dump(obj=data, fp=json_file, indent=2)


@log.timeit_if(more_than_sec=3)
def copy_bazelrc_files(user_home_dir_path, target_dir_path):
    log.info("Collecting bazel config files...")

    bazelrc_file_path = "%s/.bazelrc" % user_home_dir_path
    bazelenv_file_path = "%s/.bazelenv" % user_home_dir_path

    if path.exists(bazelrc_file_path):
        shutil.copyfile(bazelrc_file_path, "%s/user_home.bazelrc" % target_dir_path)
    else:
        log.info("%s file not found." % bazelrc_file_path)

    if path.exists(bazelenv_file_path):
        shutil.copyfile(bazelenv_file_path, "%s/user_home.bazelenv" % target_dir_path)
    else:
        log.warn("%s file expected but not found." % bazelenv_file_path)


@log.timeit_if(more_than_sec=3)
def copy_docker4mac_files(user_home_dir_path, target_dir_path):
    log.info("Collecting Docker For Mac config files...")

    settings_file_path = "%s/Library/Group Containers/group.com.docker/settings.json" % user_home_dir_path

    if path.exists(settings_file_path):
        shutil.copyfile(settings_file_path, "%s/settings.json" % target_dir_path)
    else:
        log.warn("%s file expected but not found." % settings_file_path)


@log.timeit_if(more_than_sec=5)
def snapshot():
    data = {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "user": getpass.getuser(),
        "hostname": platform.node(),
        "cpu_count": multiprocessing.cpu_count(),
        "total_ram": _get_total_ram(),
        "os": {},
        "disk": {},
        "bazel": {},
        "python": {},
    }

    output = subprocess.Popen(["df", "-H", "/"],
                              stdout=subprocess.PIPE)
    disk_line = output.communicate()[0].strip().split("\n")[1].split()
    data["disk"]["filesystem"] = disk_line[0]
    data["disk"]["total"] = disk_line[1]
    data["disk"]["used"] = disk_line[2]
    data["disk"]["free"] = disk_line[3]

    data["os"]["name"] = platform.system()
    data["os"]["version"] = platform.mac_ver()[0]

    data["bazel"]["path"] = _get_bazel_path()
    data["bazel"]["real_path"] = _get_bazel_real_path()
    data["bazel"]["version"] = _get_bazel_version()

    data["python"]["version"] = platform.python_version()
    # data["python"]["major"] = platform.python_version_tuple()[0]
    # data["python"]["minor"] = platform.python_version_tuple()[1]
    # data["python"]["patch"] = platform.python_version_tuple()[2]

    return data


def _get_os_spec():
    return oscmd.cmd_output_for(["uname", "-v"])


def _get_bazel_version():
    return oscmd.cmd_output_for(["bazel-real", "version", "--gnu_format=true"]).split()[1]


def _get_bazel_path():
    return oscmd.cmd_output_for(["which", "bazel"]).split()[0]


def _get_bazel_real_path():
    return oscmd.cmd_output_for(["which", "bazel-real"]).split()[0]


def _get_total_ram():
    raw_total_ram = oscmd.cmd_output_for(["sysctl", "hw.memsize"]).split(":")[1].strip()
    return "%dG" % (int(raw_total_ram) / (1024 * 1000 * 1024))
