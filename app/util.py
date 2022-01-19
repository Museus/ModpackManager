from pathlib import Path
import json
import shutil
import wx

from config import config
from crud import get_modpack_from_path, is_valid_modpack
from exceptions import InvalidModpack, NoModsInstalled, PathNotSelected
from smaller_util import mods_already_installed, get_mods_folder, run_modimporter


def uninstall_mods(event):
    """Uninstall currently installed mods

    Raises
    ------
    NoModsInstalled
        if no mods are installed
    """
    hades_path = Path(config["HADES"]["PATH"])

    if not mods_already_installed(hades_path):
        raise NoModsInstalled()

    mods_folder_path = get_mods_folder(hades_path)

    shutil.rmtree(mods_folder_path)
    run_modimporter(hades_path)

    window = event.GetEventObject().GetParent()
    window.FindWindowById(7).SetLabel("No modpack currently installed.")


def get_modpack_path_by_name(modpack_name):
    modpack_folder_path = config["MODPACKS"]["PATH"]
    if not config["MODPACKS"]["PATH"]:
        raise PathNotSelected()

    modpack_path = Path(modpack_folder_path) / f"{modpack_name}.zip"
    return modpack_path.resolve()


def install_selected_modpack(event: wx.CommandEvent):
    """Install modpack selected

    Parameters
    ----------
    event : [type]
        [description]
    """
    hades_path = Path(config["HADES"]["PATH"])
    modpack_path = Path(config["MODPACKS"]["SELECTED"])
    if not is_valid_modpack(modpack_path):
        raise InvalidModpack()

    modpack = get_modpack_from_path(modpack_path)

    modpack.install(hades_path)
    window = event.GetEventObject().GetParent()
    window.FindWindowById(7).SetLabel(modpack_path.stem)


def get_list_of_modpacks(modpack_folder_path: Path) -> list[Path]:
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


def get_current_modpack(hades_path: Path) -> str:
    """Get name of currently installed modpack

    Parameters
    ----------
    hades_path : Path
        path of Hades folder

    Returns
    -------
    str
        name of currently installed modpack
    """
    mods_folder_path = get_mods_folder(hades_path)
    if not mods_folder_path:
        return None

    modpack_info_file_path = mods_folder_path / "modpack.info"
    if not modpack_info_file_path.exists():
        if len(list(mods_folder_path.iterdir())) > 0:
            return "Unknown"

        return "No mods installed"

    with open(modpack_info_file_path, "r") as modpack_info_file:
        modpack_info = json.load(modpack_info_file)

    return modpack_info["name"]


def update_hades_folder_path(event: wx.FileDirPickerEvent):
    config["HADES"]["PATH"] = event.GetPath()
    with open("config.ini", "w") as config_file:
        config.write(config_file)


def update_modpack_folder_path(event: wx.FileDirPickerEvent):
    config["MODPACKS"]["PATH"] = event.GetPath()
    print(f"Updating modpack folder to: {config['MODPACKS']['PATH']}")
    with open("config.ini", "w") as config_file:
        config.write(config_file)


def update_selected_modpack(event: wx.CommandEvent):
    modpack_name = event.GetString()
    modpack_path = get_modpack_path_by_name(modpack_name)
    config["MODPACKS"]["SELECTED"] = str(modpack_path)
    with open("config.ini", "w") as config_file:
        config.write(config_file)
