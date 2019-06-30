import subprocess
from collections import namedtuple

from inspector.api.context import Context, Mode
from inspector.api.reactor import ReactorCommand
from inspector.api.tags import is_experimental, stringify, is_interactive, is_compatible_with_current_platform
from inspector.api.validator import Status
from inspector.util.cmd import execute_with_streamed_output

ExecutionSummary = namedtuple(typename="ExecutionSummary", field_names=["problem_count", "total_count"])


def _command_handler_for(ctx):
    if ctx.flags.dryrun:
        return _log_command
    else:
        return _execute_command


def _execute_command(command: ReactorCommand, ctx: Context):
    logger = ctx.logger
    logger.command_info(command)

    try:
        for line in execute_with_streamed_output(command.resolve(ctx)):
            if not command.silent:
                ctx.logger.command_output(line)

        logger.progress("Command '{}' executed successfully".format(command))
    except subprocess.CalledProcessError as err:
        logger.debug(err)
        if not command.silent:
            logger.failure("Command '{}' returned code {}".format(command, err.returncode))
    except FileNotFoundError as err:
        logger.debug(err)
        if not command.silent:
            logger.failure("Failed to execute command '{}' - {}".format(command, err))


def _log_command(command: ReactorCommand, ctx: Context):
    ctx.logger.info("\t~ {}".format(command))


_DEFAULT_CMD_HANDLER_PROVIDER = _command_handler_for


class ExecPlanExecutor:
    def execute(self, ctx: Context):
        index = 0

        for comp_id in _effective_component_ids(ctx):
            collector = _handler_or_none(ctx.registry.find_collector(comp_id), ctx)

            if collector is not None:
                index += 1
                ctx.logger.info("{} --> {}".format(index, stringify(collector)))
                validator = _handler_or_none(ctx.registry.find_validator(comp_id), ctx)
                if validator is not None:
                    index += 1
                    ctx.logger.info("{}\t --> {}".format(index, stringify(validator)))

                    reactors = ctx.registry.find_reactors(comp_id)
                    if len(reactors) == 0:
                        ctx.logger.debug("No reactors registered for {}".format(comp_id))

                    effective_reactors = (reactor for reactor in reactors if _handler_or_none(reactor, ctx) is not None)
                    for reactor in effective_reactors:
                        index += 1
                        ctx.logger.info("{}\t\t --> {}".format(index, stringify(reactor)))
                else:
                    ctx.logger.debug("No validator registered for {}".format(comp_id))


class Executor:

    def execute(self, ctx: Context, get_handler=_DEFAULT_CMD_HANDLER_PROVIDER):
        return self._exec(get_handler(ctx), ctx)

    def _exec(self, handle_command, ctx: Context):
        total = 0
        problems = 0
        for comp_id in _effective_component_ids(ctx):
            collector = _handler_or_none(ctx.registry.find_collector(comp_id), ctx)
            if collector is not None:
                data = collector.collect(ctx)

                result = self._validate(comp_id, data, ctx)
                total += 1
                if result is not None:
                    if result.status != Status.OK:
                        problems += 1
                    self._react(comp_id, result, handle_command, ctx)
                else:
                    ctx.logger.warn("{} validator produced no result!".format(comp_id))

        return ExecutionSummary(total_count=total, problem_count=problems)

    def _validate(self, comp_id, data, ctx):
        validator = _handler_or_none(ctx.registry.find_validator(comp_id), ctx)
        if validator is not None:
            return validator.validate(data, ctx)
        else:
            ctx.logger.warn("No validator is registered for {}".format(comp_id))
            return None

    def _react(self, comp_id, validation_result, handle_command, ctx):
        reactors = ctx.registry.find_reactors(comp_id)

        if len(reactors) == 0:
            ctx.logger.debug("No reactors registered for {}".format(comp_id))

        effective_reactors = list(
            reactor for reactor in reactors if _handler_or_none(reactor, ctx) is not None
        )

        for reactor in effective_reactors:
            for command in reactor.react(validation_result, ctx):
                handle_command(command, ctx)


def _handler_or_none(handler, ctx):
    if is_experimental(handler):
        if not ctx.flags.experimental:
            ctx.logger.debug("{} - filtered out, because 'experimental' flag is off!".format(stringify(handler)))
            return None

    if is_interactive(handler):
        if ctx.mode != Mode.INTERACTIVE:
            ctx.logger.warn("{} - filtered out, because it requires interactive mode!".format(stringify(handler)))
            return None

    if not is_compatible_with_current_platform(handler):
        ctx.logger.debug("{} - filtered out, because it is not compatible with the current platform!"
                         .format(stringify(handler)))
        return None

    return handler


def _effective_component_ids(ctx):
    if ctx.components is None:
        return ctx.registry.component_ids()
    else:
        return ctx.components
