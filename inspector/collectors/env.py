import getpass
import json
import multiprocessing
import platform
from datetime import datetime

from .python import PythonInfoCollector
from .bazel import BazelInfoCollector
from .os import OsInfoCollector
from .disk import DiskInfoCollector
from .hardware import HardwareInfoCollector
from util import cmd
from util import file
from util.diag import timeit_if


class EnvDataCollector:
    def __init__(self, ctx):
        self.ctx = ctx

    @timeit_if(more_than_sec=5)
    def create_snapshot_file(self, target_dir_path):
        self.ctx.logger.info("Collecting platform info...")

        data = self.snapshot()

        info_file_path = target_dir_path + "/info.json"

        with open(info_file_path, 'w') as json_file:
            json.dump(obj=data, fp=json_file, indent=2)

    @timeit_if(more_than_sec=3)
    def copy_bazelrc_files(self, user_home_dir_path, target_dir_path):
        self.ctx.logger.info("Collecting Bazel config files...")

        bazelrc_file_path = "%s/.bazelrc" % user_home_dir_path
        bazelenv_file_path = "%s/.bazelenv" % user_home_dir_path

        self._try_copy_file(bazelrc_file_path, target_dir_path, target_name_prefix="user_home")
        self._try_copy_file(bazelenv_file_path, target_dir_path, target_name_prefix="user_home")

    @timeit_if(more_than_sec=3)
    def copy_docker_config_files(self, user_home_dir_path, target_dir_path):
        self.ctx.logger.info("Collecting Docker For Mac config files...")

        settings_file_path = "%s/Library/Group Containers/group.com.docker/settings.json" % user_home_dir_path
        docker_config_file_path = "%s/.docker/config.json" % user_home_dir_path
        docker_daemon_file_path = "%s/.docker/daemon.json" % user_home_dir_path

        self._try_copy_file(settings_file_path, target_dir_path)
        self._try_copy_file(docker_config_file_path, target_dir_path)
        self._try_copy_file(docker_daemon_file_path, target_dir_path)

    @timeit_if(more_than_sec=5)
    def snapshot(self):
        hw_info = HardwareInfoCollector(self.ctx).collect()
        data = {
            "timestamp_utc": datetime.utcnow().isoformat(),
            "user": getpass.getuser(),
            "hostname": platform.node(),
            "cpu_count": hw_info.cpu_count,
            "total_ram": hw_info.total_ram,
            "os": {},
            "disk": {},
            "bazel": {},
            "python": {},
        }

        disk_info = DiskInfoCollector(self.ctx).collect()
        data["disk"]["filesystem"] = disk_info.filesystem
        data["disk"]["total"] = disk_info.total
        data["disk"]["used"] = disk_info.used
        data["disk"]["free"] = disk_info.free

        os_info = OsInfoCollector(self.ctx).collect()
        data["os"]["name"] = os_info.name
        data["os"]["version"] = str(os_info.version)

        bazel_info = BazelInfoCollector(self.ctx).collect()
        data["bazel"]["path"] = bazel_info.path
        data["bazel"]["real_path"] = bazel_info.real_path
        data["bazel"]["version"] = str(bazel_info.version)

        python_info = PythonInfoCollector(self.ctx).collect()
        data["python"]["path"] = str(python_info.path)
        data["python"]["version"] = str(python_info.version)

        return data

    def _try_copy_file(self, source_file_path, target_dir_path, target_name_prefix=""):
        if not file.try_copy_file(source_file_path, target_dir_path, target_name_prefix):
            self.ctx.logger.warn("%s file expected but not found." % source_file_path)
