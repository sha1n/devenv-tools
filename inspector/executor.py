from inspector.commons.context import Context
from inspector.collectors.basecollector import Collector
from inspector.validators.basevalidator import Validator
from inspector.reactors.basereactor import Reactor


class Executor:
    def __init__(self):
        self._collectors = {}
        self._validators = {}
        self._reactors = {}

    def register_collector(self, component_id, collector: Collector):
        self._collectors[component_id] = collector

    def register_validator(self, component_id, validator: Validator):
        self._validators[component_id] = validator

    def register_reactor(self, component_id, *reactors: Reactor):
        existing_reactors = self._reactors.get(component_id, [])
        self._reactors[component_id] = existing_reactors + list(reactors)

    def execute(self, ctx: Context) -> int:
        try:
            self._exec(ctx)
            return 0

        except Exception as err:
            ctx.logger.failure("Failure! %s" % err)
            return 1

    def _exec(self, ctx: Context):
        for name in self._collectors.keys():
            collector = self._collectors[name]
            data = collector.collect()

            result = self._validate(name, data)
            if result is not None:
                self._react(name, result, ctx)

    def _validate(self, name, data):
        validator = self._validators.get(name, None)
        if validator is not None:
            return validator.validate(data)
        else:
            return None

    def _react(self, name, validation_result, ctx):
        # fixme: if not ctx.dryrun:
        for reactor in self._reactors.get(name, []):
            for command in reactor.react(validation_result):
                ctx.logger.info("\t~ {}".format(command))  # fixme should execute...
