from datetime import datetime
from pathlib import Path
from tempfile import TemporaryFile
from zipfile import ZipFile, Path as ZipfilePath
import logging
import json

from exceptions import ModsAlreadyInstalled
from smaller_util import (
    get_content_folder,
    get_mods_folder,
    mods_already_installed,
    run_modimporter,
)


class Modpack:
    def __init__(self, modpack_path: Path):
        self.path = modpack_path.resolve()
        self.zip_file = ZipFile(modpack_path)
        modpack_zip_path = ZipfilePath(self.zip_file)

        self.modimporter_path = modpack_zip_path / "modimporter.py"
        self.mods_folder_path = modpack_zip_path / "Mods"

    @property
    def mods(self):
        return [mod.name for mod in self.mods_folder_path.iterdir() if mod.is_dir()]

    def install(self, hades_path: Path):
        if mods_already_installed(hades_path):
            raise ModsAlreadyInstalled()

        self.extract_mods(hades_path)
        self.create_modpack_info(hades_path)
        self.extract_modimporter(hades_path)

        run_modimporter(hades_path)

    def extract_mods(self, hades_path: Path, mods_folder_name: str = "Mods"):
        content_path = get_content_folder(hades_path)

        print("Extracting mods.")
        for file_name in self.zip_file.namelist():
            if not file_name.startswith(f"{mods_folder_name}/"):
                continue

            self.zip_file.extract(self.zip_file.getinfo(file_name), path=content_path)

        print("Finished extracting mods.")

    def extract_modimporter(
        self, hades_path: Path, modimporter_name: str = "modimporter.py"
    ):
        content_path = get_content_folder(hades_path)

        print("Extracting modimporter.")
        self.zip_file.extract(
            self.zip_file.getinfo(modimporter_name), path=content_path
        )
        print("Finished extracting modimporter.")

    def create_modpack_info(self, hades_path: Path):
        modpack_name = self.path.stem.replace("_", " ")
        modpack_install_date = str(datetime.utcnow().isoformat())
        mods_folder_path = get_mods_folder(hades_path)

        modpack_info = {
            "name": modpack_name,
            "installed": modpack_install_date,
        }

        with open(mods_folder_path / "modpack.info", "w") as modpack_info_file:
            json.dump(modpack_info, modpack_info_file)

    @classmethod
    def is_valid(cls, modpack_path: Path):
        zip_file = ZipFile(modpack_path)
        if not any(zip_item.startswith("Mods/") for zip_item in zip_file.namelist()):
            logging.error("Selected zip file does not have a Mods folder")
            return False

        if not any(zip_item == "modimporter.py" for zip_item in zip_file.namelist()):
            logging.error("Selected zip file does not have a modimporter")
            return False

        return True
