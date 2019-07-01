import functools

from shminspector.util.logger import ConsoleLogger, Logger, NOOP_LOGGER

_logger = ConsoleLogger()


def try_wrap(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        error = None
        try:
            result = func(*args, **kwargs)
        except Exception as err:
            error = err

        return result, error

    return wrapper


def raised_to_none_wrapper(func, logger: Logger = NOOP_LOGGER):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_func = try_wrap(func)
        result, error = new_func(*args, **kwargs)
        if error is not None:
            logger.warn(error)

        return result

    return wrapper
