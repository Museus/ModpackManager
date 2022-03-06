from pathlib import Path
import shutil

import wx

from config import config
from util.classes import HadesPath, Modpack
from util.exceptions import InvalidModpack, NoModsInstalled


def available_modpacks(modpack_folder_path: Path) -> list[Path]:
    """Get list of modpacks in specified folder

    Parameters
    ----------
    modpack_folder_path : Path
        Path object for modpack directory

    Returns
    -------
    list[Path]
        list of individual modpack Path objects
    """
    modpacks = []

    for file_path in modpack_folder_path.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix == ".zip":
            modpacks.append(file_path.stem)

    return modpacks


def get_modpack_path_by_name(modpack_name: str) -> Path:
    """Get Path pointing at specified modpack zip file

    Parameters
    ----------
    modpack_name : str
        name of modpack to find

    Returns
    -------
    Path
        path to modpack zip file

    Raises
    ------
    PathNotSelected
        No mods folder path selected
    """
    pass


def install_selected_modpack(event: wx.CommandEvent):
    """

    Parameters
    ----------
    event : wx.CommandEvent
        event triggered by clicking "Install" button
    """
    hades_path = HadesPath(config["HADES"]["PATH"])
    modpack_path = Path(config["MODPACKS"]["SELECTED"])

    if not Modpack.is_valid(modpack_path):
        raise InvalidModpack()

    if hades_path.mods_already_installed():
        uninstall_mods(event)

    modpack = Modpack(modpack_path)

    modpack.install(hades_path)
    window = event.GetEventObject().GetParent()
    window.FindWindowById(7).SetLabel(modpack_path.stem)


def uninstall_mods(event: wx.CommandEvent):
    """Uninstall currently installed mods

    Raises
    ------
    NoModsInstalled
        if no mods are installed
    """
    hades_path = HadesPath(config["HADES"]["PATH"])

    if not hades_path.mods_already_installed():
        raise NoModsInstalled()

    mods_folder_path = hades_path.mods_folder

    shutil.rmtree(mods_folder_path)
    hades_path.run_modimporter()

    window = event.GetEventObject().GetParent()
    window.FindWindowById(7).SetLabel("No modpack currently installed.")
