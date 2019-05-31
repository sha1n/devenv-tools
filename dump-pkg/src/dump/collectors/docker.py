from dump.collectors.files import try_copyfile, file_path, mkdir
from inspector.util.cmd import try_capture_output, command


def collect_docker_files(user_home_dir_path, target_dir_path, ctx):
    if command("docker"):
        ctx.logger.info("Collecting Docker information...")

        mkdir(target_dir_path)

        _collect_version(target_dir_path, ctx)
        _collect_info(target_dir_path, ctx)

        if ctx.snapshot.docker_configured():
            ctx.logger.info("Collecting Docker files...")
            _collect_config_files(target_dir_path, user_home_dir_path, ctx)
    else:
        ctx.logger.warn("'docker' not installed")


def _collect_config_files(target_dir_path, user_home_dir_path, ctx):
    ctx.logger.progress("Collecting configuration files...")

    source_settings_file_path = file_path(user_home_dir_path, "Library/Group Containers/group.com.docker/settings.json")
    target_settings_file_path = file_path(target_dir_path, "settings.json")
    try_copyfile(source_settings_file_path, target_settings_file_path)

    source_docker_config_file_path = file_path(user_home_dir_path, ".docker/config.json")
    target_docker_config_file_path = file_path(target_dir_path, "config.json")
    try_copyfile(source_docker_config_file_path, target_docker_config_file_path)

    source_docker_daemon_file_path = file_path(user_home_dir_path, ".docker/daemon.json")
    target_docker_daemon_file_path = file_path(target_dir_path, "daemon.json")
    try_copyfile(source_docker_daemon_file_path, target_docker_daemon_file_path)


def _collect_version(target_dir, ctx):
    ctx.logger.progress("Collecting version information...")
    return try_capture_output(cmd=["docker", "version"],
                              target_dir_path=target_dir,
                              file_name="docker_version.txt",
                              logger=ctx.logger)


def _collect_info(target_dir, ctx):
    ctx.logger.progress("Collecting docker information...")
    return try_capture_output(cmd=["docker", "info"],
                              target_dir_path=target_dir,
                              file_name="docker_info.txt",
                              logger=ctx.logger)
