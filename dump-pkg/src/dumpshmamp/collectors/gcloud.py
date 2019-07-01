from dumpshmamp.collectors.files import try_copytree_if, try_copyfile, file_path, mkdir
from shminspector.util.cmd import try_capture_output, is_command

two_week_sec = 14 * 24 * 60 * 60  # days * hours * minutes * seconds


def collect_gcloud_files(user_home_dir, target_dir, ctx):
    if not ctx.snapshot.gcloud_configured():
        return

    mkdir(target_dir)
    ctx.logger.info("Collecting gcloud files...")

    _collect_logs(user_home_dir, target_dir, ctx)
    _collect_config(user_home_dir, target_dir, ctx)
    _collect_info(target_dir, ctx)


def _collect_logs(user_home_dir, target_dir, ctx):
    ctx.logger.progress("Copying gcloud log files...")
    try_copytree_if(
        source_dir="{}/.config/gcloud/logs".format(user_home_dir),
        target_dir="{}/logs".format(target_dir),
        modified_in_the_past_sec=two_week_sec,
        logger=ctx.logger
    )


def _collect_config(user_home_dir, target_dir, ctx):
    ctx.logger.progress("Copying selected gcloud config files...")

    source_config_default_path = file_path(user_home_dir, ".config/gcloud/configurations/config_default")
    target_config_default_path = file_path(target_dir, "config_default")
    try_copyfile(source_config_default_path, target_config_default_path, logger=ctx.logger)

    source_active_config_path = file_path(user_home_dir, ".config/gcloud/active_config")
    target_config_default_path = file_path(target_dir, "active_default")
    try_copyfile(source_active_config_path, target_config_default_path, logger=ctx.logger)


def _collect_info(target_dir, ctx):
    if is_command("gcloud"):
        try_capture_output(
            cmd=["gcloud", "info"],
            additional_env={
                "LANG": "en_US.UTF-8",
                "LC_ALL": "en_US.UTF-8",
            },
            target_dir_path=target_dir,
            file_name="gcloud_info.txt",
            logger=ctx.logger
        )
    else:
        ctx.logger.debug("'gcloud' not installed")
