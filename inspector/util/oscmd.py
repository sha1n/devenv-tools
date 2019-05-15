import subprocess


def cmd_output_for(cmd):
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output.communicate()[0].strip()
