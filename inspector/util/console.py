import functools
from time import time


def info(text):
    print("\033[1;37;40mINFO\033[0;0m: %s" % text)


def warn(text):
    print("\033[1;33;40mWARN\033[0;0m: %s" % text)


def error(text):
    print("\033[1;31;40mERRO\033[0;0m: %s" % text)


def success(text):
    print("\033[1;37;40mINFO\033[0;0m: \033[0;30;42m%s\033[0;0m" % text)


def failure(text):
    print("\033[1;31;40mERRO\033[0;0m: \033[0;37;41m%s\033[0;0m" % text)


def _debug_time(text):
    print("\033[0;37;40mDEBG\033[0;0m: %s\033[0;0m" % text)


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
                    msg = "Function '%s' from [%s] took %f secs" % (func.__name__, module, run_time)

                if more_than_sec != 0:
                    _debug_time(msg)
                else:
                    info(msg)

            return value

        return wrapper_timer

    return t


def timeit(func):
    return timeit_if()(func)
