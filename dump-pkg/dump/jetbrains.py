import json
import os
import time
from collections import namedtuple
from os import listdir
from shutil import copyfile
from shutil import copytree

from inspector.api.context import Context
from inspector.util import file
from inspector.util.diag import timeit_if

two_week_sec = 14 * 24 * 60 * 60  # days * hours * minutes * seconds

JetBrainsProductInfo = namedtuple(
    typename="JetBrainsProductInfo",
    field_names=["name", "log_dir_segment", "pref_dir_segment"]
)


class JetBrainsProductDataCollector:
    def __init__(self, product_info: JetBrainsProductInfo, ctx: Context):
        self.ctx = ctx
        self.product_info = product_info

    @timeit_if(more_than_sec=20)
    def collect_info_files(self, user_home_dir_path, target_dir_path):
        self.ctx.logger.info("Collecting {} product(s) info...".format(self.product_info.name))
        for file_path in self._collect_product_info_files():
            version = self._read_json_property(file_path, "version")
            code = self._read_json_property(file_path, "productCode")
            copyfile(file_path,
                     "{}/{}-{}-{}-product-info.json".format(target_dir_path, self.product_info.name, code, version))

        self.ctx.logger.log(
            "Collecting {} logs... (files older than two weeks will be ignored)".format(self.product_info.name))
        for logs_dir_path in self._collect_log_libraries(user_home_dir_path):
            dir_name = file.name_from(logs_dir_path)

            self.ctx.logger.log("Copying {}...".format(logs_dir_path))
            copytree(
                src=logs_dir_path,
                dst="{}/logs/{}".format(target_dir_path, dir_name),
                ignore=self._ignore_files_mtime_gt(two_week_sec)
            )

        self.ctx.logger.log("Collecting {} configuration files...".format(self.product_info.name))
        for config_dir_path in self._collect_configurations(user_home_dir_path):
            dir_name = file.name_from(config_dir_path)

            self.ctx.logger.log("Copying {}...".format(config_dir_path))
            copytree(config_dir_path, "{}/configs/{}".format(target_dir_path, dir_name))

    @timeit_if(more_than_sec=3)
    def _collect_product_info_files(self):
        candidates = listdir("/Applications")

        return (
            "/Applications/" + ij_app_dir + "/Contents/Resources/product-info.json"
            for ij_app_dir in candidates if ij_app_dir.find(self.product_info.name) == 0
        )

    @timeit_if(more_than_sec=10)
    def _collect_log_libraries(self, user_home):
        candidates = listdir("{}/Library/Logs".format(user_home))

        return (
            "{}/Library/Logs/{}".format(user_home, ij_logs_dir)
            for ij_logs_dir in candidates if ij_logs_dir.find(self.product_info.log_dir_segment) != -1
        )

    def _collect_configurations(self, user_home):
        candidates = listdir("{}/Library/Preferences".format(user_home))

        return (
            "{}/Library/Preferences/{}".format(user_home, ij_prefs_dir)
            for ij_prefs_dir in candidates if ij_prefs_dir.find(self.product_info.pref_dir_segment) != -1
        )

    @staticmethod
    def _read_json_property(file_path, property_name):
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data[property_name]

    @staticmethod
    def _ignore_files_mtime_gt(interval_sec):
        def ignore(path, names):
            return (name for name in names if os.path.getmtime("{}/{}".format(path, name)) < time.time() - interval_sec)

        return ignore
