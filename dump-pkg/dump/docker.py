from dump.files import try_copy_file
from inspector.util.cmd import capture_output


def copy_docker_files(user_home_dir_path, target_dir_path, ctx):
    ctx.logger.info("Collecting Docker For Mac config files...")

    _collect_config_files(target_dir_path, user_home_dir_path, ctx)
    _collect_info(target_dir_path, ctx)
    _collect_version(target_dir_path, ctx)


def _collect_config_files(target_dir_path, user_home_dir_path, ctx):
    ctx.logger.log("Collecting configuration files...")

    settings_file_path = "{}/Library/Group Containers/group.com.docker/settings.json".format(user_home_dir_path)
    if not try_copy_file(settings_file_path, target_dir_path):
        ctx.logger.warn("{} file expected but not found.".format(settings_file_path))

    docker_config_file_path = "{}/.docker/config.json".format(user_home_dir_path)
    if not try_copy_file(docker_config_file_path, target_dir_path):
        ctx.logger.warn("{} file expected but not found.".format(docker_config_file_path))

    docker_daemon_file_path = "{}/.docker/daemon.json".format(user_home_dir_path)
    if not try_copy_file(docker_daemon_file_path, target_dir_path):
        ctx.logger.warn("{} file expected but not found.".format(docker_daemon_file_path))


def _collect_version(target_dir, ctx):
    ctx.logger.log("Collecting version info...")
    capture_output(cmd=["docker", "version"], target_dir_path=target_dir, file_name="docker_version.txt", ctx=ctx)


def _collect_info(target_dir, ctx):
    ctx.logger.log("Collecting docker info...")
    capture_output(cmd=["docker", "info"], target_dir_path=target_dir, file_name="docker_info.txt", ctx=ctx)
