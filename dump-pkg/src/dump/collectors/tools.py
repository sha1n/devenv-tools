from inspector.util.cmd import try_capture_output


def collect_shell_tools_info_files(target_dir, ctx):
    ctx.logger.info("Collecting shell tools info...")

    _collect_info(["bash", "--version"], target_dir, "bash_version.txt", ctx)
    _collect_info(["gcc", "--version"], target_dir, "gcc_version.txt", ctx)
    _collect_info(["tar", "--version"], target_dir, "tar_version.txt", ctx)


def _collect_info(cmd, target_dir, file_name, ctx):
    try_capture_output(
        cmd=cmd,
        target_dir_path=target_dir,
        file_name=file_name,
        logger=ctx.logger
    )
