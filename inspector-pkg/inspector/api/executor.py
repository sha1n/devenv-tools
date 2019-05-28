import os

from inspector.api.context import Context


class Executor:

    def execute(self, ctx: Context) -> int:
        try:
            self._exec(ctx)
            return 0

        except Exception as err:
            ctx.logger.failure("Failure! %s" % err)
            return 1

    @staticmethod
    def _exec(ctx: Context):
        for comp_id in ctx.registry.component_ids():
            collector = ctx.registry.find_collector(comp_id)
            data = collector.collect()

            result = Executor._validate(comp_id, data, ctx)
            if result is not None:
                Executor._react(comp_id, result, ctx)

    @staticmethod
    def _validate(name, data, ctx):
        validator = ctx.registry.find_validator(name)
        if validator is not None:
            return validator.validate(data)
        else:
            return None

    @staticmethod
    def _react(comp_id, validation_result, ctx):
        def exec_with(fn):
            for reactor in ctx.registry.find_reactors(comp_id):
                for command in reactor.react(validation_result):
                    fn(command, ctx)

        if ctx.dryrun:
            exec_with(Executor._log_command)
        else:
            exec_with(Executor._execute_command)

    @staticmethod
    def _execute_command(command, ctx):
        ctx.logger.info("Executing command:\n\t~ {}".format(command))
        code = os.system(str(command))

        if code != 0 and not command.silent:
            ctx.logger.failure("Exit code {}".format(code))

    @staticmethod
    def _log_command(command, ctx):
        ctx.logger.info("\t~ {}".format(command))
