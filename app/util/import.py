import os
from pathlib import Path
import shutil

from . import get_mods_folder
from exceptions import NoModsInstalled


def mods_already_installed(hades_path: Path) -> bool:
    """Check if mods are already installed"""
    mods_path = hades_path / "Mods"
    installed_mods = list(mods_path.iterdir())
    return installed_mods > 0


def run_modimporter(hades_path: Path):
    """Switch working directory to hades_path and run the modimporter script there

    Parameters
    ----------
    hades_path : Path
        path to Hades folder
    """
    current_working_directory = os.getcwd()
    os.chdir(hades_path)

    with open("modimporter.py") as modimporter:
        exec(modimporter.read())

    os.chdir(current_working_directory)


def uninstall_mods(hades_path):
    mods_folder_path = get_mods_folder(hades_path)
    if not mods_folder_path:
        raise NoModsInstalled()

    shutil.rmtree(mods_folder_path)
    run_modimporter(hades_path)
