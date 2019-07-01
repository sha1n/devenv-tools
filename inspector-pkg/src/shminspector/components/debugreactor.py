from shminspector.api.context import Context
from shminspector.api.reactor import Reactor
from shminspector.api.validator import ValidationResult


class DebugReactor(Reactor):

    def react(self, data: ValidationResult, ctx: Context):
        ctx.logger.debug("Validation result: {}. Data = {}".format(data.status.name, data.input_data))
        return []
