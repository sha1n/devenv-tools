import json
import os.path as path
from collections import namedtuple

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.tags import macos
from inspector.api.validator import Validator, ValidationResult, Status
from inspector.components.command import command_collector, command_validator
from inspector.util import cmd


@macos
@command_collector("gcloud")
@command_validator("gcloud")
class GCloudCommandCollectorValidator:
    pass


GCloudConfig = namedtuple(
    typename="GCloudConfig",
    field_names=["account", "auth_ok", "docker_ok"]
)


@macos
class GCloudConfigCollector(Collector):
    _expected_cred_helpers = {
        "us.gcr.io": "gcloud",
        "asia.gcr.io": "gcloud",
        "marketplace.gcr.io": "gcloud",
        "staging-k8s.gcr.io": "gcloud",
        "gcr.io": "gcloud",
        "eu.gcr.io": "gcloud"
    }

    def collect(self, ctx: Context):
        account = self._account(ctx)
        if account is not None:
            return GCloudConfig(account=account, auth_ok=self._auth_ok(ctx, account), docker_ok=self._docker_ok())
        else:
            return None

    def _auth_ok(self, ctx, expected_account):
        ok, code, output = cmd.try_execute(cmd=["gcloud", "auth", "list", "--format", "json"], logger=ctx.logger)

        if ok and code == 0:
            auth_list_json = json.loads(output)
            for entry in auth_list_json:
                if entry["account"] == expected_account and entry["status"] == "ACTIVE":
                    return True

        return False

    def _docker_ok(self):
        docker_config_path = path.join(path.expanduser("~"), ".docker", "config.json")
        config_exists = path.exists(docker_config_path)
        if config_exists:
            with open(docker_config_path, "r") as config_file:
                config = json.load(config_file)

            actual_cred_helpers = config.get("credHelpers", {})
            for key in self._expected_cred_helpers.keys():
                if self._expected_cred_helpers[key] != actual_cred_helpers.get(key, None):
                    return False

        return config_exists

    def _account(self, ctx):
        ok, code, output = cmd.try_execute(cmd=["gcloud", "config", "get-value", "account", "--format", "json"],
                                           logger=ctx.logger)
        if ok and code == 0:
            return output.strip().strip('"')
        else:
            return None


@macos
class GCloudConfigValidator(Validator):
    def validate(self, input_data, ctx: Context) -> ValidationResult:
        if input_data is None or \
                not input_data.docker_ok or \
                not input_data.auth_ok:
            return ValidationResult(input_data, Status.NOT_FOUND)
        else:
            return ValidationResult(input_data, Status.OK)
