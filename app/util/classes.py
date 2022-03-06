from datetime import datetime
from hashlib import md5
from pathlib import Path
from zipfile import ZipFile, Path as ZipfilePath
import json
import logging
import subprocess
import time

from util.exceptions import InvalidModimporter, ModsAlreadyInstalled, UnknownHadesPath
from util.core_util import (
    working_directory,
)


class HadesPath:
    def __init__(self, path: str):
        self.path = Path(path)

    @property
    def content_folder(self) -> Path:
        """Try to detect Content folder from specified Hades path

        Returns
        -------
        Path
            Path to Content if it can be detected

        Raises
        ------
        UnknownHadesPath
            if Content Path isn't found
        """
        if not self.path.exists():
            logging.error("Could not find Hades path")

        if self.path.name == "Content":
            return self.path

        if self.path.name == "Hades":
            return self.path / "Content"

        if self.path.name == "Mods":
            return self.path.parent

        raise UnknownHadesPath("Could not find Content Path")

    @property
    def mods_folder(self) -> Path:
        """Get Mods path from specified Hades path

        Returns
        -------
        Path
            Path to Mods if it can be detected

        Raises
        ------
        UnknownHadesPath
            if Mods Path isn't found
        """
        mods_folder_path = self.content_folder / "Mods"
        mods_folder_path.mkdir(exist_ok=True)

        if not mods_folder_path.exists():
            logging.error("Could not find or create Mods folder")
            raise UnknownHadesPath("Failed to find or create Mods folder")

        return mods_folder_path

    @property
    def current_modpack(self) -> str:
        """Get name of currently installed modpack

        Returns
        -------
        str
            name of currently installed modpack
        """
        if not self.mods_folder:
            return "No mods installed"

        modpack_info_file_path = self.mods_folder / "modpack.info"
        if not modpack_info_file_path.exists():
            if len(list(self.mods_folder.iterdir())) > 0:
                return "Unknown mods installed"

            return "No mods installed"

        with open(modpack_info_file_path, "r") as modpack_info_file:
            modpack_info = json.load(modpack_info_file)

        return modpack_info["name"]

    def mods_already_installed(self) -> bool:
        """Check if mods are already installed"""
        installed_mods = len(list(self.mods_folder.iterdir()))
        logging.debug(f"Number of currently installed mods: {installed_mods}")
        return installed_mods > 0

    def run_modimporter(self):
        """Switch working directory to hades_path and run the modimporter script there"""
        with working_directory(self.content_folder):
            modimport_process = subprocess.Popen(
                "modimporter.py", stdin=subprocess.PIPE, shell=True
            )
            while modimport_process.poll() is None:
                time.sleep(0.25)
                modimport_process.communicate(b"\n")


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

    @classmethod
    def is_valid(cls, modpack_path: HadesPath):
        zip_file = ZipFile(modpack_path)
        if not any(zip_item.startswith("Mods/") for zip_item in zip_file.namelist()):
            logging.error("Selected zip file does not have a Mods folder")
            return False

        if not any(zip_item == "modimporter.py" for zip_item in zip_file.namelist()):
            logging.error("Selected zip file does not have a modimporter")
            return False

        return True

    def install(self, hades_path: HadesPath):
        """Install this modpack to the specified Hades path

        Parameters
        ----------
        hades_path : Path
            Path to install Modpack

        Raises
        ------
        ModsAlreadyInstalled
            [description]
        """
        if hades_path.mods_already_installed():
            raise ModsAlreadyInstalled()

        self.extract_mods(hades_path)
        self.create_modpack_info(hades_path)
        self.extract_modimporter(hades_path)

        hades_path.run_modimporter()

    def extract_mods(self, hades_path: HadesPath, mods_folder_name: str = "Mods"):
        content_path = hades_path.content_folder

        logging.debug("Extracting mods from {self.path.name} to Mods folder")
        for file_name in self.zip_file.namelist():
            if (
                not file_name.startswith(f"{mods_folder_name}/")
                or file_name == f"{mods_folder_name}/"
            ):
                continue

            self.zip_file.extract(self.zip_file.getinfo(file_name), path=content_path)

        logging.debug("Finished extracting mods.")

    def extract_modimporter(
        self, hades_path: HadesPath, modimporter_name: str = "modimporter.py"
    ):
        logging.debug("Extracting modimporter from {self.path.name} to Mods folder")

        extracted_modimporter = self.zip_file.extract(
            self.zip_file.getinfo(modimporter_name), path=hades_path.content_folder
        )

        with (
            open(extracted_modimporter, "rb") as modimporter_file,
            open("legal_modimporters.txt", "r") as legal_modimporters,
        ):
            hashed_modimporter = md5(modimporter_file.read()).hexdigest()
            legal_hashes = [
                legal_hash.strip() for legal_hash in legal_modimporters.readlines()
            ]

        if hashed_modimporter not in legal_hashes:
            Path(extracted_modimporter).unlink()
            raise InvalidModimporter()

        logging.debug("Finished extracting modimporter.")

    def create_modpack_info(self, hades_path: HadesPath):
        modpack_name = self.path.stem.replace("_", " ")
        modpack_install_date = str(datetime.utcnow().isoformat())
        mods_folder_path = hades_path.mods_folder

        modpack_info = {
            "name": modpack_name,
            "installed": modpack_install_date,
        }

        with open(mods_folder_path / "modpack.info", "w") as modpack_info_file:
            json.dump(modpack_info, modpack_info_file)
