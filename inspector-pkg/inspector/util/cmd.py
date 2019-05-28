import subprocess


def execute(cmd):
    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

    if completed_process.returncode != 0:
        raise Exception("Failed to execute command '{}'!".format(cmd))

    return completed_process.stdout


def try_execute(cmd):
    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

    return completed_process.returncode, completed_process.stdout
