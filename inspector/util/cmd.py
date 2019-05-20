import subprocess


def execute(cmd):
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output.communicate()[0].strip()
