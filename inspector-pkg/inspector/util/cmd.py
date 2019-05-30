import subprocess

from inspector.util.logger import NOOP_LOGGER


def execute(cmd):
    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

    if completed_process.returncode != 0:
        raise Exception("Failed to execute command '{}'!".format(cmd))

    return completed_process.stdout


def try_execute(cmd, logger=NOOP_LOGGER):
    try:
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

        return True, completed_process.returncode, completed_process.stdout
    except FileNotFoundError as err:
        logger.warn(err)
        return False, -1, None


def try_capture_output(cmd, target_dir_path, file_name, logger=NOOP_LOGGER):
    cmd_string = " ".join(cmd)

    ok, code, stdout = try_execute(cmd, logger)

    if not ok:
        logger.warn("Failed to execute '{}'".format(cmd_string))
    elif code != 0:
        logger.warn("'{}' returned code {}".format(cmd_string, code))
    else:
        target_file_path = "{}/{}".format(target_dir_path, file_name)
        logger.log("Writing '{}' to {}".format(cmd_string, target_file_path))
        with open(target_file_path, 'w') as info_file:
            info_file.write(stdout)
