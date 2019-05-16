import getpass
import multiprocessing
import socket
import subprocess
import json

import oscmd


def create_snapshot_file(target_dir_path):
    info = snapshot()

    info_file_path = target_dir_path + "/platform-info.json"

    with open(info_file_path, 'w') as json_file:
        json.dump(obj=info, fp=json_file, indent=2)


def snapshot():
    info = {
        "user": getpass.getuser(),
        "hostname": socket.gethostname(),
        "cpu_count": multiprocessing.cpu_count(),
        "total_ram": _get_total_ram(),
        "disk": {},
    }

    output = subprocess.Popen(["df", "-H", "/"],
                              stdout=subprocess.PIPE)
    disk_line = output.communicate()[0].strip().split("\n")[1].split()
    info["disk"]["filesystem"] = disk_line[0]
    info["disk"]["total"] = disk_line[1]
    info["disk"]["used"] = disk_line[2]
    info["disk"]["free"] = disk_line[3]
    info["os_spec"] = _get_os_spec()
    info["bazel_version"] = _get_bazel_version()

    return info


def _get_os_spec():
    return oscmd.cmd_output_for(["uname", "-v"])


def _get_bazel_version():
    return oscmd.cmd_output_for(["bazel-real", "version", "--gnu_format=true"]).split()[1]


def _get_total_ram():
    raw_total_ram = oscmd.cmd_output_for(["sysctl", "hw.memsize"]).split(":")[1].strip()
    return "%dG" % (int(raw_total_ram) / (1024 * 1000 * 1024))
