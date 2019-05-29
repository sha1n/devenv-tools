from inspector.api.context import Context
from inspector.util.cmd import try_execute


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
            else:
                ctx.logger.warn("{} validator produced no result!".format(comp_id))

    @staticmethod
    def _validate(comp_id, data, ctx):
        validator = ctx.registry.find_validator(comp_id)
        if validator is not None:
            return validator.validate(data)
        else:
            ctx.logger.warn("No validator registered for {}".format(comp_id))
            return None

    @staticmethod
    def _react(comp_id, validation_result, ctx):
        def exec_with(fn):
            reactors = ctx.registry.find_reactors(comp_id)

            if len(reactors) == 0:
                ctx.logger.debug("No reactors registered for {}".format(comp_id))

            for reactor in reactors:
                for command in reactor.react(validation_result):
                    fn(command, ctx)

        if ctx.dryrun:
            exec_with(Executor._log_command)
        else:
            exec_with(Executor._execute_command)

    @staticmethod
    def _execute_command(command, ctx):
        ctx.logger.log_os_command(command)
        code, stdout = try_execute(command.cmd)

        if not command.silent:
            ctx.logger.log_command_output(stdout)

            if code != 0:
                ctx.logger.failure("Command {} returned code {}".format(command, code))

    @staticmethod
    def _log_command(command, ctx):
        ctx.logger.info("\t~ {}".format(command))
