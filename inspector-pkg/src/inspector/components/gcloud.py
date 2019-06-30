import json
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
    field_names=["account", "auth_ok"]
)


@macos
class GCloudConfigCollector(Collector):
    def collect(self, ctx: Context):
        account = self._account(ctx)
        if account is not None:
            return GCloudConfig(account=account, auth_ok=self._auth_ok(ctx, account))
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
        if input_data is None:
            return ValidationResult(input_data, Status.NOT_FOUND)
        else:
            return ValidationResult(input_data, Status.OK)
