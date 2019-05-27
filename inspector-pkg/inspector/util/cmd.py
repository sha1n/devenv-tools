import subprocess


def execute(cmd):
    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

    if completed_process.returncode != 0:
        raise Exception("Shit...")

    return completed_process.stdout
