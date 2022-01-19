from pathlib import Path
import contextlib
import logging
import os
import subprocess

from exceptions import UnknownHadesPath


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def mods_already_installed(hades_path: Path) -> bool:
    """Check if mods are already installed"""
    mods_path = get_mods_folder(hades_path)
    installed_mods = len(list(mods_path.iterdir()))
    logging.debug(f"Number of currently installed mods: {installed_mods}")
    return installed_mods > 0


def run_modimporter(hades_path: Path):
    """Switch working directory to hades_path and run the modimporter script there

    Parameters
    ----------
    hades_path : Path
        path to Hades folder
    """
    content_folder = get_content_folder(hades_path)
    with working_directory(content_folder):
        subprocess.call("modimporter.py", shell=True)


def get_mods_folder(hades_path: Path) -> Path:
    content_folder_path = get_content_folder(hades_path)

    mods_folder_path = content_folder_path / "Mods"
    mods_folder_path.mkdir(exist_ok=True)

    if not mods_folder_path.exists():
        logging.error("Could not find or create Mods folder")
        raise UnknownHadesPath()

    return mods_folder_path


def get_content_folder(hades_path: Path) -> Path:
    if not hades_path.exists():
        logging.error("Could not find Hades path")

    if hades_path.name == "Content":
        return hades_path

    if hades_path.name == "Hades":
        return hades_path / "Content"

    if hades_path.name == "Mods":
        return hades_path.parent

    raise UnknownHadesPath()
