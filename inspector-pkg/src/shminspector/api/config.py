import json

_DEFAULT_CONFIG = {
    "hardware": {
        "minimum_cpu_count": 8,
        "minimum_total_ram_gb": 16,
    },
    "network": {
        "check_specs": [
            {
                "address": "http://www.google.com",
                "failure_message": "Public network access check failed! Make sure you are connected to a network",
            },
        ],
    },
    "installer": {
        "python": {
            "macos_package_url": "https://www.python.org/ftp/python/3.6.8/python-3.6.8-macosx10.9.pkg"
        },
        "docker": {
            "macos_package_url": "https://download.docker.com/mac/stable/Docker.dmg"
        }
    }
}


def load(config_file):
    if config_file is not None:
        with open(config_file, "r") as json_config_file:
            return json.load(json_config_file)
    else:
        return _DEFAULT_CONFIG
