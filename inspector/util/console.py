
def info(text):
  print("\033[0;37;40mINFO: %s" % text)

def success(text):
  print("\033[1;32;40mINFO: %s" % text)  

def warn(text):
  print("\033[1;33;40mWARN: %s" % text)

def error(text):
  print("\033[1;31;40mERRO: %s" % text)