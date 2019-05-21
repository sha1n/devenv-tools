import functools
from time import time


_ERASE_LINE = '\x1b[2K'


class Console:
    def input(self, prompt):
        pass

    @staticmethod
    def log(message):
        print("\033[1;37;40mINFO\033[0;0m: {}".format(message), end="\r")

    @staticmethod
    def debug(message):
        print("{}\033[0;37;40mDEBG\033[0;0m: {}\033[0;0m".format(_ERASE_LINE, message))

    @staticmethod
    def info(message):
        print("{}\033[1;37;40mINFO\033[0;0m: {}".format(_ERASE_LINE, message))

    @staticmethod
    def warn(message):
        print("{}\033[1;33;40mWARN\033[0;0m: {}".format(_ERASE_LINE, message))

    @staticmethod
    def error(message):
        print("{}\033[1;31;40mERRO\033[0;0m: {}".format(_ERASE_LINE, message))

    @staticmethod
    def success(message):
        print("{}\033[1;37;40mINFO\033[0;0m: \033[0;30;42m{}\033[0;0m".format(_ERASE_LINE, message))

    @staticmethod
    def failure(message):
        print("{}\033[1;31;40mERRO\033[0;0m: \033[0;37;41m{}\033[0;0m".format(_ERASE_LINE, message))


def _debug_time(text):
    print("\n\033[0;37;40mDEBG\033[0;0m: %s\033[0;0m" % text)


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
                    Console.debug(msg)
                else:
                    Console.info(msg)

            return value

        return wrapper_timer

    return t


def timeit(func):
    return timeit_if()(func)
