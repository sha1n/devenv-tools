import json
import os
from collections import namedtuple
from os import listdir

from dump.collectors.files import try_copytree_if, try_copytree, file_name_from, try_copyfile
from inspector.api.context import Context
from inspector.util.diag import timeit_if

two_week_sec = 14 * 24 * 60 * 60  # days * hours * minutes * seconds

JetBrainsProductInfo = namedtuple(
    typename="JetBrainsProductInfo",
    field_names=["name", "log_dir_segment", "pref_dir_segment"]
)


class JetBrainsProductDataCollector:
    def __init__(self, product_info: JetBrainsProductInfo, user_home_dir_path, target_dir_path, ctx: Context):
        self.ctx = ctx
        self.product_info = product_info
        self.user_home_dir_path = user_home_dir_path
        self.target_dir_path = target_dir_path

    def collect(self):
        product_info_files = list(self._collect_product_info_file_paths())
        if len(product_info_files) > 0:
            self._collect_product_files(product_info_files, self.target_dir_path, self.user_home_dir_path)

    def _collect_product_files(self, product_info_files, target_dir_path, user_home_dir_path):
        os.mkdir(target_dir_path)
        self.ctx.logger.info("{} installation detected! Collecting files...".format(self.product_info.name))
        self._copy_product_info_files(product_info_files, target_dir_path)
        self._copy_log_files(target_dir_path, user_home_dir_path)
        self._copy_config_files(target_dir_path, user_home_dir_path)

    @timeit_if(more_than_sec=10)
    def _copy_config_files(self, target_dir_path, user_home_dir_path):
        self.ctx.logger.progress("Collecting {} configuration files...".format(self.product_info.name))

        for config_dir_path in self._collect_configuration_dir_paths(user_home_dir_path):
            dir_name = file_name_from(config_dir_path)

            self.ctx.logger.progress("Copying {}...".format(config_dir_path))
            try_copytree(
                source_dir=config_dir_path,
                target_dir="{}/configs/{}".format(
                    target_dir_path,
                    dir_name
                ),
                logger=self.ctx.logger
            )

    @timeit_if(more_than_sec=10)
    def _copy_log_files(self, target_dir_path, user_home_dir_path):
        self.ctx.logger.progress(
            "Collecting {} logs... (files older than two weeks will be ignored)".format(self.product_info.name))

        for logs_dir_path in self._collect_log_dir_paths(user_home_dir_path):
            dir_name = file_name_from(logs_dir_path)

            self.ctx.logger.progress("Copying {}...".format(logs_dir_path))
            try_copytree_if(
                source_dir=logs_dir_path,
                target_dir="{}/logs/{}".format(target_dir_path, dir_name),
                modified_in_the_past_sec=two_week_sec,
                logger=self.ctx.logger
            )

    @timeit_if(more_than_sec=10)
    def _copy_product_info_files(self, product_info_files, target_dir_path):
        self.ctx.logger.progress("Collecting {} product info files...".format(self.product_info.name))

        for file_path in product_info_files:
            version = self._read_json_property(file_path, "version")
            code = self._read_json_property(file_path, "productCode")
            try_copyfile(
                source_file=file_path,
                target_file="{}/{}-{}-{}-product-info.json".format(
                    target_dir_path,
                    self.product_info.name,
                    code,
                    version
                ),
                logger=self.ctx.logger
            )

    def _collect_product_info_file_paths(self):
        candidates = listdir("/Applications")

        return (
            "/Applications/" + ij_app_dir + "/Contents/Resources/product-info.json"
            for ij_app_dir in candidates if ij_app_dir.find(self.product_info.name) == 0
        )

    def _collect_log_dir_paths(self, user_home):
        candidates = listdir("{}/Library/Logs".format(user_home))

        return (
            "{}/Library/Logs/{}".format(user_home, ij_logs_dir)
            for ij_logs_dir in candidates if ij_logs_dir.find(self.product_info.log_dir_segment) != -1
        )

    def _collect_configuration_dir_paths(self, user_home):
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
