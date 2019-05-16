def info(text):
    print("\033[1;37;40mINFO\033[0;0m: %s" % text)


def warn(text):
    print("\033[1;33;40mWARN\033[0;0m: %s" % text)


def error(text):
    print("\033[1;31;40mERRO\033[0;0m: %s" % text)


def success(text):
    print("\033[1;37;40mINFO: \033[0;30;42m%s\033[0;0m" % text)


def failure(text):
    print("\033[1;31;40mERRO: \033[0;37;41m%s\033[0;0m" % text)
