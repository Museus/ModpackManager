from pathlib import Path
import unittest

from app.util import get_list_of_modpacks, mods_in_modpack


class TestUtil(unittest.TestCase):
    def test_get_list_of_modpacks(self):
        EXPECTED_MODPACKS = [
            "HyperDelivery1_Modpack",
            "HyperDelivery2_Modpack",
            "HyperDelivery3_Modpack",
            "HyperDelivery4_Modpack",
            "HyperDelivery5_Modpack",
            "HyperDelivery6_Modpack",
        ]

        test_modpacks_path = Path("test/test_modpacks")
        modpacks = [
            modpack.stem for modpack in get_list_of_modpacks(test_modpacks_path)
        ]

        self.assertEqual(sorted(modpacks), sorted(EXPECTED_MODPACKS))

    def test_mods_in_invalid_modpack(self):
        EXPECTED_MODS = [
            "EllosBoonSelectorMod",
            "InfiniDD",
            "MinibossControl",
            "ModUtil",
            "PrintUtil",
            "RemoveCutscenes",
            "RemoveThanatos",
            "SatyrSackControl",
            "ShowChamberNumber",
        ]

        test_modpack_path = Path("test/test_modpacks/HyperDelivery1_Modpack.zip")
        test_mods = [mod.name for mod in mods_folder_contents(test_modpack_path)]

        self.assertEqual(sorted(test_mods), sorted(EXPECTED_MODS))

    def test_mods_in_modpack(self):
        EXPECTED_MODS = [
            "EllosBoonSelectorMod",
            "InfiniDD",
            "MinibossControl",
            "ModUtil",
            "PrintUtil",
            "RemoveCutscenes",
            "RemoveThanatos",
            "SatyrSackControl",
            "ShowChamberNumber",
        ]

        test_modpack_path = Path("test/test_modpacks/HyperDelivery1_Modpack.zip")
        test_mods = [mod.name for mod in mods_in_modpack(test_modpack_path)]

        self.assertEqual(sorted(test_mods), sorted(EXPECTED_MODS))


if __name__ == "__main__":
    unittest.main()
