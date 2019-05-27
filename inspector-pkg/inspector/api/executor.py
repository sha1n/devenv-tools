from inspector.api.context import Context


class Executor:

    def execute(self, ctx: Context) -> int:
        try:
            self._exec(ctx)
            return 0

        except Exception as err:
            ctx.logger.failure("Failure! %s" % err)
            return 1

    def _exec(self, ctx: Context):
        for comp_id in ctx.registry.component_ids():
            collector = ctx.registry.find_collector(comp_id)
            data = collector.collect()

            result = self._validate(comp_id, data, ctx)
            if result is not None:
                self._react(comp_id, result, ctx)

    @staticmethod
    def _validate(name, data, ctx):
        validator = ctx.registry.find_validator(name)
        if validator is not None:
            return validator.validate(data)
        else:
            return None

    @staticmethod
    def _react(comp_id, validation_result, ctx):
        # fixme: if not ctx.dryrun:
        for reactor in ctx.registry.find_reactors(comp_id):
            for command in reactor.react(validation_result):
                ctx.logger.info("\t~ {}".format(command))  # fixme should execute...
