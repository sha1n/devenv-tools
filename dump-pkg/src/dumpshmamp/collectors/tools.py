from dumpshmamp.collectors.files import mkdir

from shminspector.util.cmd import try_capture_output, is_command


def collect_shell_tools_info_files(target_dir, ctx):
    ctx.logger.info("Collecting shell tools information...")

    mkdir(target_dir)

    _collect_info(["brew", "--config"], target_dir, "brew_config.txt", ctx)
    _collect_info(["brew", "doctor", "--debug"], target_dir, "brew_doctor_debug.txt", ctx)
    _collect_info(["bash", "--version"], target_dir, "bash_version.txt", ctx)
    _collect_info(["gcc", "--version"], target_dir, "gcc_version.txt", ctx)
    _collect_info(["clang", "--version"], target_dir, "clang_version.txt", ctx)
    _collect_info(["tar", "--version"], target_dir, "tar_version.txt", ctx)
    _collect_info(["java", "-version"], target_dir, "java_version.txt", ctx)
    _collect_info(["mvn", "--version"], target_dir, "mvn_version.txt", ctx)
    _collect_info(["xcode-select", "-p"], target_dir, "xcode_select.txt", ctx)
    _collect_info(["softwareupdate", "-l"], target_dir, "softwareupdate_l.txt", ctx)
    _collect_info(["env"], target_dir, "env.txt", ctx)


def _collect_info(cmd, target_dir, file_name, ctx):
    executable_name = cmd[0]
    if is_command(executable_name):
        try_capture_output(
            cmd=cmd,
            target_dir_path=target_dir,
            file_name=file_name,
            logger=ctx.logger
        )
    else:
        ctx.logger.warn("'{}' not installed".format(executable_name))
