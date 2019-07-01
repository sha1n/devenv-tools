import functools
from time import time

from shminspector.util.logger import ConsoleLogger

_logger = ConsoleLogger()


def timeit_if(more_than_sec=0, alt_text=None):
    def t(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time()
            value = func(*args, **kwargs)
            end_time = time()
            run_time = end_time - start_time
            if run_time >= more_than_sec:
                module = func.__module__
                msg = alt_text
                if msg is None:
                    msg = "Function '{}' from [{}] took {} secs. args: {}, kwargs: {}".format(
                        func.__name__,
                        module,
                        run_time,
                        args,
                        kwargs
                    )

                if more_than_sec != 0:
                    _logger.debug(msg)
                else:
                    _logger.info(msg)

            return value

        return wrapper_timer

    return t


def timeit(func):
    return timeit_if()(func)
