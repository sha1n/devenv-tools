from dump.collectors.files import file_path, try_copyfile, mkdir


def collect_bazel_files(user_home_dir_path, target_dir_path, ctx):
    if not ctx.snapshot.bazel_installed():
        return

    ctx.logger.info("Collecting Bazel config files...")

    mkdir(target_dir_path)

    source_bazelrc_file_path = file_path(user_home_dir_path, ".bazelrc")
    source_bazelenv_file_path = file_path(user_home_dir_path, ".bazelenv")

    target_bazelrc_file_path = file_path(target_dir_path, ".bazelrc")
    target_bazelenv_file_path = file_path(target_dir_path, ".bazelenv")

    try_copyfile(source_bazelrc_file_path, target_bazelrc_file_path, logger=ctx.logger)
    try_copyfile(source_bazelenv_file_path, target_bazelenv_file_path, logger=ctx.logger)
