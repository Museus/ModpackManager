import configparser
import logging
from pathlib import Path

from exceptions import NoConfigFound


def create_default_config(config, config_ini_path):
    config["HADES"] = {
        "path": "",
    }

    config["MODPACKS"] = {
        "path": "",
        "selected": "",
    }
    with open(config_ini_path, "w") as config_file:
        config.write(config_file)

    return config


config = configparser.ConfigParser()
try:
    config_ini_path = Path("config.ini")
    config.read(Path("config.ini"))
    if not ("HADES" in config and "MODPACKS" in config):
        raise NoConfigFound()
except NoConfigFound:
    create_default_config(config, config_ini_path)
    logging.warning("Failed to parse config, generating a new one")
