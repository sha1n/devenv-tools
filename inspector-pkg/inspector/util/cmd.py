import subprocess


def execute(cmd):
    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

    if completed_process.returncode != 0:
        raise Exception("Failed to execute command '{}'!".format(cmd))

    return completed_process.stdout


def try_execute(cmd):
    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

    return completed_process.returncode, completed_process.stdout


def capture_output(cmd, target_dir_path, file_name, ctx):
    code, stdout = try_execute(cmd)

    if code != 0:
        ctx.logger.warn("'{}' returned code {}".format(" ".join(cmd), code))
    else:
        target_file_path = "{}/{}".format(target_dir_path, file_name)
        ctx.logger.log("Writing gcloud info to {}".format(target_file_path))
        with open(target_file_path, 'w') as info_file:
            info_file.write(stdout)
