import os.path as path
import tempfile
from urllib.parse import urlparse

from shminspector.api.reactor import ReactorCommand


def download_and_install_commands_for(url):
    commands = []

    download_command, pkg_file = download_command_for(url)
    commands.append(download_command)
    commands.append(install_pkg_command_for(pkg_file))

    return commands


def download_command_for(url):
    target_dir = tempfile.mkdtemp(prefix="envinstaller-")

    parsed_url = urlparse(url)
    file_name = path.basename(parsed_url.path)
    target_file_path = path.join(target_dir, file_name)

    return ReactorCommand(["curl", "-s", "--compressed", "-o", target_file_path, url]), target_file_path


def mount_command_for(dmg_file):
    return ReactorCommand(["sudo", "hdiutil", "attach", dmg_file])


def install_pkg_command_for(pkg_file):
    return ReactorCommand(["sudo", "installer", "-pkg", pkg_file, "-target", "/"])
