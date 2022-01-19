from pathlib import Path
import json

from . import get_mods_folder


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

    modpack_info_file = mods_folder_path / "modpack.info"
    if not modpack_info_file.exists():
        return "Unknown"

    modpack_info = json.load(modpack_info_file)
    return modpack_info["name"]
