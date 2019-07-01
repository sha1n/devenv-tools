import getpass
import json
import os
import platform
from datetime import datetime

import dumpshmamp.collectors.files as files
from dumpshmamp.collectors.bazel import collect_bazel_files
from dumpshmamp.collectors.docker import collect_docker_files
from dumpshmamp.collectors.gcloud import collect_gcloud_files
from dumpshmamp.collectors.tools import collect_shell_tools_info_files
from shminspector.components.bazel import BazelInfoCollector
from shminspector.components.disk import DiskInfoCollector
from shminspector.components.hardware import HardwareInfoCollector
from shminspector.components.network import UrlConnectivityInfoCollector
from shminspector.components.os import OsInfoCollector
from shminspector.components.python import PythonInfoCollector
from shminspector.util.diag import timeit_if


class Snapshot:
    def __init__(self, data):
        self.data = data

    def bazel_installed(self):
        return "path" in self.data["bazel"]

    def gcloud_configured(self):
        return "configured" in self.data["gcloud"] and self.data["gcloud"]["configured"] is True

    def docker_configured(self):
        return "configured" in self.data["docker"] and self.data["docker"]["configured"] is True


class EnvDataCollector:
    def __init__(self, ctx, user_home_dir_path, target_dir_path):
        self.ctx = ctx
        self.user_home_dir_path = user_home_dir_path
        self.target_dir_path = target_dir_path

    def collect(self):
        self.ctx.logger.info("Collecting environment information...")
        env_info_target_dir_path = self.target_dir_path

        self.ctx.logger.info("Collecting platform information...")
        snapshot = self.snapshot()
        self.ctx.snapshot = snapshot

        self._create_snapshot_file(snapshot, env_info_target_dir_path)

        bazel_files_dir_path = "{}/bazel".format(env_info_target_dir_path)
        self._copy_bazelrc_files(bazel_files_dir_path)

        docker_files_dir_path = "{}/docker".format(env_info_target_dir_path)
        self._copy_docker_config_files(docker_files_dir_path)

        gcloud_files_dir_path = "{}/gcloud".format(env_info_target_dir_path)
        self._copy_gcloud_files(gcloud_files_dir_path)

        tools_files_dir_path = "{}/tools".format(env_info_target_dir_path)
        collect_shell_tools_info_files(tools_files_dir_path, self.ctx)

    @timeit_if(more_than_sec=5)
    def _create_snapshot_file(self, snapshot, target_dir_path):
        info_file_path = target_dir_path + "/info.json"

        with open(info_file_path, 'w') as json_file:
            json.dump(obj=snapshot.data, fp=json_file, indent=2)

    @timeit_if(more_than_sec=3)
    def _copy_bazelrc_files(self, target_dir_path):
        collect_bazel_files(self.user_home_dir_path, target_dir_path, self.ctx)

    @timeit_if(more_than_sec=3)
    def _copy_docker_config_files(self, target_dir_path):
        collect_docker_files(self.user_home_dir_path, target_dir_path, self.ctx)

    @timeit_if(more_than_sec=3)
    def _copy_gcloud_files(self, target_dir_path):
        collect_gcloud_files(self.user_home_dir_path, target_dir_path, self.ctx)

    @timeit_if(more_than_sec=5)
    def snapshot(self):

        data = {
            "timestamp_utc": datetime.utcnow().isoformat(),
            "user": getpass.getuser(),
            "hostname": platform.node(),
            "cpu_count": "",
            "total_ram": "",
            "os": {},
            "disk": {},
            "bazel": {},
            "python": {},
            "gcloud": {},
            "docker": {},
            "network": {}
        }

        data["gcloud"]["configured"] = files.path_exists("{}/.config/gcloud".format(self.user_home_dir_path))
        data["docker"]["configured"] = files.path_exists("{}/.docker".format(self.user_home_dir_path))
        data["docker"]["server_installed"] = files.path_exists("/var/run/docker.sock")

        net_connectivity_info_collector = UrlConnectivityInfoCollector()
        results = []
        data["network"]["connectivity_checks"] = results
        for result in net_connectivity_info_collector.collect(self.ctx):
            results.append({
                "address": result.address,
                "ok": result.ok,
                "time": result.time
            })

        def set_hw_info(hw_info):
            data["cpu_count"] = hw_info.cpu_count
            data["total_ram"] = hw_info.total_ram

        self._try_collect(HardwareInfoCollector(), set_hw_info)

        def set_disk_info(disk_info):
            data["disk"]["filesystem"] = disk_info.filesystem
            data["disk"]["total"] = disk_info.total
            data["disk"]["used"] = disk_info.used
            data["disk"]["free"] = disk_info.free

        self._try_collect(DiskInfoCollector(), set_disk_info)

        def set_os_info(os_info):
            data["os"]["name"] = os_info.name
            data["os"]["version"] = str(os_info.version)

        self._try_collect(OsInfoCollector(), set_os_info)

        def set_bazel_info(bazel_info):
            data["bazel"]["path"] = bazel_info.path
            data["bazel"]["bazelisk"] = bazel_info.bazelisk
            data["bazel"]["version"] = str(bazel_info.version)
            data["bazel"]["env.USE_BAZEL_VERSION"] = os.environ.get("USE_BAZEL_VERSION", "N/A")

        self._try_collect(collector=BazelInfoCollector(),
                          action=set_bazel_info,
                          not_found_message="'bazel' not installed")

        def set_python_info(python_info):
            data["python"]["path"] = str(python_info.path)
            data["python"]["version"] = str(python_info.version)

        self._try_collect(collector=PythonInfoCollector(),
                          action=set_python_info,
                          not_found_message="'python' not installed")

        return Snapshot(data)

    def _try_collect(self, collector, action, not_found_message="No data collected"):
        try:
            result = collector.collect(self.ctx)
            if result is not None:
                action(result)
            else:
                self.ctx.logger.warn(not_found_message)
        except Exception as err:
            self.ctx.logger.warn(
                "Failed to collect data. collector={}, error={}".format(collector.__class__.__name__, err))
