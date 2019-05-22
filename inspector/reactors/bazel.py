from inspector.reactors.basereactor import Reactor
from inspector.validators.basevalidator import ValidationResult, Status
from inspector.util.context import Context


class BazelValidationLogReactor(Reactor):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def react(self, data: ValidationResult):
        if data.status != Status.OK:
            self.logger.warn("Incompatible Bazel version: {}".format(str(data.input_data.version)))


class BazelValidationInstallReactor(Reactor):
    def __init__(self, ctx: Context):
        super().__init__(ctx)

    def react(self, data: ValidationResult):
        if data.status == Status.NOT_FOUND:
            self.install()
        elif data.status.UPGRADE_REQUIRED:
            self.upgrade()
        elif data.status.DOWNGRADE_REQUIRED:
            self.uninstall()
            self.install()

    def install(self): raise NotImplementedError

    def upgrade(self): raise NotImplementedError

    def uninstall(self): raise NotImplementedError
