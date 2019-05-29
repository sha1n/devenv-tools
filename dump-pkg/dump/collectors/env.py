import getpass
import json
import os
import platform
from datetime import datetime

import dump.collectors.docker as docker
import dump.collectors.gcloud as gcloud
from dump.collectors.files import try_copy_file
from inspector.components.bazel import BazelInfoCollector
from inspector.components.disk import DiskInfoCollector
from inspector.components.hardware import HardwareInfoCollector
from inspector.components.network import UrlConnectivityInfoCollector
from inspector.components.os import OsInfoCollector
from inspector.components.python import PythonInfoCollector
from inspector.util.diag import timeit_if


class EnvDataCollector:
    def __init__(self, ctx, user_home_dir_path, target_dir_path):
        self.ctx = ctx
        self.user_home_dir_path = user_home_dir_path
        self.target_dir_path = target_dir_path

    def collect(self):
        self.ctx.logger.info("Collecting environment info...")
        env_info_target_dir_path = self.target_dir_path

        self._create_snapshot_file(env_info_target_dir_path)

        user_home_bazel_files_dir_path = "{}/bazel".format(env_info_target_dir_path)
        os.makedirs(user_home_bazel_files_dir_path)
        self._copy_bazelrc_files(user_home_bazel_files_dir_path)

        user_home_d4m_files_dir_path = "{}/docker".format(env_info_target_dir_path)
        os.mkdir(user_home_d4m_files_dir_path)
        self._copy_docker_config_files(user_home_d4m_files_dir_path)

        user_home_gcloud_files_dir_path = "{}/gcloud".format(env_info_target_dir_path)
        os.mkdir(user_home_gcloud_files_dir_path)
        self._copy_gcloud_files(user_home_gcloud_files_dir_path)

    @timeit_if(more_than_sec=5)
    def _create_snapshot_file(self, target_dir_path):
        self.ctx.logger.info("Collecting platform info...")

        data = self.snapshot()

        info_file_path = target_dir_path + "/info.json"

        with open(info_file_path, 'w') as json_file:
            json.dump(obj=data, fp=json_file, indent=2)

    @timeit_if(more_than_sec=3)
    def _copy_bazelrc_files(self, target_dir_path):
        self.ctx.logger.info("Collecting Bazel config files...")

        bazelrc_file_path = "%s/.bazelrc" % self.user_home_dir_path
        bazelenv_file_path = "%s/.bazelenv" % self.user_home_dir_path

        self._try_copy_file(bazelrc_file_path, target_dir_path, target_name_prefix="user_home")
        self._try_copy_file(bazelenv_file_path, target_dir_path, target_name_prefix="user_home")

    @timeit_if(more_than_sec=3)
    def _copy_docker_config_files(self, target_dir_path):
        docker.copy_docker_files(self.user_home_dir_path, target_dir_path, self.ctx)

    @timeit_if(more_than_sec=3)
    def _copy_gcloud_files(self, target_dir_path):
        gcloud.collect_files(self.user_home_dir_path, target_dir_path, self.ctx)

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

        data["gcloud"]["configured"] = os.path.exists("{}/.config/gcloud".format(self.user_home_dir_path))
        data["docker"]["configured"] = os.path.exists("{}/.docker".format(self.user_home_dir_path))
        data["docker"]["server_installed"] = os.path.exists("/var/run/docker.sock")

        net_connectivity_info_collector = UrlConnectivityInfoCollector(ctx=self.ctx)
        results = []
        data["network"]["connectivity_checks"] = results
        for result in net_connectivity_info_collector.collect():
            results.append({
                "address": result.address,
                "ok": result.ok,
                "time": result.time
            })

        def set_hw_info(hw_info):
            data["cpu_count"] = hw_info.cpu_count
            data["total_ram"] = hw_info.total_ram

        self._try_collect(HardwareInfoCollector(self.ctx), set_hw_info)

        def set_disk_info(disk_info):
            data["disk"]["filesystem"] = disk_info.filesystem
            data["disk"]["total"] = disk_info.total
            data["disk"]["used"] = disk_info.used
            data["disk"]["free"] = disk_info.free

        self._try_collect(DiskInfoCollector(self.ctx), set_disk_info)

        def set_os_info(os_info):
            data["os"]["name"] = os_info.name
            data["os"]["version"] = str(os_info.version)

        self._try_collect(OsInfoCollector(self.ctx), set_os_info)

        def set_bazel_info(bazel_info):
            data["bazel"]["path"] = bazel_info.path
            data["bazel"]["bazelisk"] = bazel_info.bazelisk
            data["bazel"]["version"] = str(bazel_info.version)

        self._try_collect(collector=BazelInfoCollector(self.ctx),
                          action=set_bazel_info,
                          not_found_message="Bazel not found!")

        def set_python_info(python_info):
            data["python"]["path"] = str(python_info.path)
            data["python"]["version"] = str(python_info.version)

        self._try_collect(collector=PythonInfoCollector(self.ctx),
                          action=set_python_info,
                          not_found_message="Python not found!")

        return data

    def _try_copy_file(self, source_file_path, target_dir_path, target_name_prefix=""):
        if not try_copy_file(source_file_path, target_dir_path, target_name_prefix):
            self.ctx.logger.warn("%s file expected but not found." % source_file_path)

    def _try_collect(self, collector, action, not_found_message="No data collected"):
        try:
            result = collector.collect()
            if result is not None:
                action(result)
            else:
                self.ctx.logger.warn(not_found_message)
        except Exception as err:
            self.ctx.logger.warn(
                "Failed to collect data. collector={}, error={}".format(collector.__class__.__name__, err))
