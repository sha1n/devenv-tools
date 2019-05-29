from dump.files import copytree_if, try_copy_file

two_week_sec = 14 * 24 * 60 * 60  # days * hours * minutes * seconds


def collect_files(user_home_dir, target_dir, ctx):
    _collect_logs(user_home_dir, target_dir, ctx)
    _collect_config(user_home_dir, target_dir, ctx)


def _collect_logs(user_home_dir, target_dir, ctx):
    ctx.logger.log("Copying gcloud log files...")
    copytree_if(
        source_dir="{}/.config/gcloud/logs".format(user_home_dir),
        target_dir="{}/logs".format(target_dir),
        modified_in_the_past_sec=two_week_sec
    )


def _collect_config(user_home_dir, target_dir, ctx):
    ctx.logger.log("Copying selected gcloud config files...")
    config_default_path = "{}/.config/gcloud/configurations/config_default".format(user_home_dir)
    if not try_copy_file(config_default_path, target_dir):
        ctx.logger.warn("{} file expected but not found.".format(config_default_path))

    active_config_path = "{}/.config/gcloud/active_config".format(user_home_dir)
    if not try_copy_file(active_config_path, target_dir):
        ctx.logger.warn("{} file expected but not found.".format(config_default_path))
