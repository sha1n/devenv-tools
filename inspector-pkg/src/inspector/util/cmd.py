import os
import shutil
import subprocess

from inspector.util.logger import NOOP_LOGGER


def is_command(executable_name):
    return shutil.which(executable_name) is not None


def execute(cmd, additional_env=None):
    completed_process = subprocess.run(cmd,
                                       env=_envvars(additional_env),
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       encoding='utf-8')

    if completed_process.returncode != 0:
        raise Exception("Failed to execute command '{}'! output: {}".format(cmd, completed_process.stdout))

    return completed_process.stdout


def try_execute(cmd, additional_env=None, logger=NOOP_LOGGER):

    try:
        completed_process = subprocess.run(cmd,
                                           env=_envvars(additional_env),
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT,
                                           encoding='utf-8')

        return True, completed_process.returncode, completed_process.stdout
    except FileNotFoundError as err:
        logger.debug(err)
        return False, -1, None


def try_capture_output(cmd, target_dir_path, file_name, additional_env=None, logger=NOOP_LOGGER):
    cmd_string = " ".join(cmd)

    ok, code, output = try_execute(cmd, additional_env=additional_env, logger=logger)

    if not ok:
        logger.warn("Failed to execute '{}'".format(cmd_string))
    else:
        if code != 0:
            logger.warn("'{}' returned code {}".format(cmd_string, code))

        target_file_path = "{}/{}".format(target_dir_path, file_name)
        logger.progress("Writing '{}' to {}".format(cmd_string, target_file_path))
        with open(target_file_path, 'w') as info_file:
            info_file.write(output)

    return ok


def execute_with_streamed_output(cmd, additional_env=None):
    popen = subprocess.Popen(cmd,
                             env=_envvars(additional_env),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             universal_newlines=True)
    for line in iter(popen.stdout.readline, ""):
        yield line

    popen.stdout.close()

    return_code = popen.wait()
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, cmd)


def _envvars(custom=None):
    effective_env = custom
    if custom is not None:
        return {**custom, **os.environ.copy()}

    return effective_env
