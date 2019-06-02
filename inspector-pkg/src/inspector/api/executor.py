from inspector.api.context import Context
from inspector.api.reactor import ReactorCommand
from inspector.util.cmd import try_execute


def _command_handler_for(ctx):
    if ctx.dryrun:
        return _log_command
    else:
        return _execute_command


def _execute_command(command: ReactorCommand, ctx: Context):
    logger = ctx.logger
    logger.command_info(command)
    ok, code, stdout = try_execute(command.cmd, logger)

    if not command.silent:
        logger.command_output(stdout)

        if ok:
            if code != 0:
                logger.failure("Command '{}' returned code {}".format(command, code))
            else:
                logger.progress("Command '{}' executed successfully (return code = {})".format(command, code))
        else:
            logger.failure("Failed to execute command '{}'".format(command))


def _log_command(command: ReactorCommand, ctx: Context):
    ctx.logger.info("\t~ {}".format(command))


_DEFAULT_CMD_HANDLER_PROVIDER = _command_handler_for


class Executor:

    def execute(self, ctx: Context, get_handler=_DEFAULT_CMD_HANDLER_PROVIDER):
        Executor._exec(get_handler(ctx), ctx)

    @staticmethod
    def _exec(handle_command, ctx: Context):
        for comp_id in ctx.registry.component_ids():
            collector = ctx.registry.find_collector(comp_id)
            data = collector.collect(ctx)

            result = Executor._validate(comp_id, data, ctx)
            if result is not None:
                Executor._react(comp_id, result, handle_command, ctx)
            else:
                ctx.logger.warn("{} validator produced no result!".format(comp_id))

    @staticmethod
    def _validate(comp_id, data, ctx):
        validator = ctx.registry.find_validator(comp_id)
        if validator is not None:
            return validator.validate(data, ctx)
        else:
            ctx.logger.warn("No validator registered for {}".format(comp_id))
            return None

    @staticmethod
    def _react(comp_id, validation_result, handle_command, ctx):
        reactors = ctx.registry.find_reactors(comp_id)

        if len(reactors) == 0:
            ctx.logger.debug("No reactors registered for {}".format(comp_id))

        for reactor in reactors:
            for command in reactor.react(validation_result, ctx):
                handle_command(command, ctx)

    @staticmethod
    def _execute_command(command, ctx):
        ctx.logger.command_info(command)
        ok, code, stdout = try_execute(command.cmd, ctx.logger)

        if not command.silent:
            ctx.logger.command_output(stdout)

            if ok:
                if code != 0:
                    ctx.logger.failure("Command '{}' returned code {}".format(command, code))
                else:
                    ctx.logger.progress("Command '{}' executed successfully (return code = {})".format(command, code))
            else:
                ctx.logger.failure("Failed to execute command '{}'".format(command))

    @staticmethod
    def _log_command(command, ctx):
        ctx.logger.info("\t~ {}".format(command))
