import os.path as path
import tempfile
from urllib.parse import urlparse

from inspector.api.reactor import ReactorCommand


def download_and_install_commands_for(url):
    commands = []
    target_dir = tempfile.mkdtemp(prefix="envinstaller-")

    parsed_url = urlparse(url)
    file_name = path.basename(parsed_url.path)
    pkg_file = path.join(target_dir, file_name)

    commands.append(ReactorCommand(["curl", "-s", "--compressed", "-o", pkg_file, url]))
    commands.append(ReactorCommand(["sudo", "installer", "-pkg", pkg_file, "-target", "/"]))

    return commands
