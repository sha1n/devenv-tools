import getpass
import json
import multiprocessing
import platform
from datetime import datetime

from util import cmd
from util import console as log
from util import file


@log.timeit_if(more_than_sec=5)
def create_snapshot_file(target_dir_path):
    log.info("Collecting platform info...")

    data = snapshot()

    info_file_path = target_dir_path + "/info.json"

    with open(info_file_path, 'w') as json_file:
        json.dump(obj=data, fp=json_file, indent=2)


@log.timeit_if(more_than_sec=3)
def copy_bazelrc_files(user_home_dir_path, target_dir_path):
    log.info("Collecting bazel config files...")

    bazelrc_file_path = "%s/.bazelrc" % user_home_dir_path
    bazelenv_file_path = "%s/.bazelenv" % user_home_dir_path

    file.try_copy_file(bazelrc_file_path, target_dir_path, target_name_prefix="user_home")
    file.try_copy_file(bazelenv_file_path, target_dir_path, target_name_prefix="user_home")


@log.timeit_if(more_than_sec=3)
def copy_docker_config_files(user_home_dir_path, target_dir_path):
    log.info("Collecting Docker For Mac config files...")

    settings_file_path = "%s/Library/Group Containers/group.com.docker/settings.json" % user_home_dir_path
    docker_config_file_path = "%s/.docker/config.json" % user_home_dir_path
    docker_daemon_file_path = "%s/.docker/daemon.json" % user_home_dir_path

    file.try_copy_file(settings_file_path, target_dir_path)
    file.try_copy_file(docker_config_file_path, target_dir_path)
    file.try_copy_file(docker_daemon_file_path, target_dir_path)


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

    disk_line = cmd.execute(["df", "-H", "/"]).split("\n")[1].split()
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

    return data


def _get_bazel_version():
    return cmd.execute(["bazel-real", "version", "--gnu_format=true"]).split()[1]


def _get_bazel_path():
    return cmd.execute(["which", "bazel"]).split()[0]


def _get_bazel_real_path():
    return cmd.execute(["which", "bazel-real"]).split()[0]


def _get_total_ram():
    raw_total_ram = cmd.execute(["sysctl", "hw.memsize"]).split(":")[1].strip()
    return "%dG" % (int(raw_total_ram) / (1024 * 1000 * 1024))
