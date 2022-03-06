import logging
from pathlib import Path

import wx

from config import config
from util.exceptions import PathNotSelected
from util.classes import HadesPath
from util.util import (
    available_modpacks,
    install_selected_modpack,
    uninstall_mods,
)


class SelectModpackFrame(wx.Frame):
    """
    A Frame that allows the user to select a modpack
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super().__init__(*args, **kw)

        # create a panel in the frame
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # put some text with a larger bold font on it
        static_text_current_modpack_header = wx.StaticText(
            panel, label="Current Modpack"
        )
        font = static_text_current_modpack_header.GetFont()
        font.PointSize += 5
        font = font.Bold()
        static_text_current_modpack_header.SetFont(font)

        static_text_current_modpack_name = wx.StaticText(panel, label="Unknown", id=7)
        static_text_current_modpack_name.SetLabel(
            HadesPath(config["HADES"]["path"]).current_modpack
        )
        button_uninstall_current_modpack = wx.Button(panel, label="Uninstall")
        button_uninstall_current_modpack.Bind(wx.EVT_BUTTON, uninstall_mods)

        static_text_configuration_header = wx.StaticText(
            panel, label="Path Configuration"
        )
        font = static_text_configuration_header.GetFont()
        font.PointSize += 5
        font = font.Bold()
        static_text_configuration_header.SetFont(font)

        static_text_hades_folder = wx.StaticText(
            panel, label="Hades Directory", name="HadesFolderStaticText"
        )
        folder_picker_hades_folder = wx.DirPickerCtrl(
            panel, path=config["HADES"]["PATH"], name="HadesFolderPicker"
        )
        folder_picker_hades_folder.Bind(
            wx.EVT_DIRPICKER_CHANGED, self.update_hades_folder_path
        )

        static_text_modpack_folder = wx.StaticText(
            panel, label="Modpack Folder", name="ModpackFolderStaticText"
        )
        folder_picker_modpack_folder = wx.DirPickerCtrl(
            panel, path=config["MODPACKS"]["PATH"], name="ModpackFolderPicker"
        )
        folder_picker_modpack_folder.Bind(
            wx.EVT_DIRPICKER_CHANGED, self.update_modpack_folder_path
        )

        static_text_choose_modpack_header = wx.StaticText(
            panel, label="Modpack to Install"
        )
        font = static_text_choose_modpack_header.GetFont()
        font.PointSize += 5
        font = font.Bold()
        static_text_choose_modpack_header.SetFont(font)

        combo_box_choose_modpack = get_combo_box_choose_modpack(panel, config)
        combo_box_choose_modpack.Bind(wx.EVT_COMBOBOX, self.update_selected_modpack)

        button_install_modpack = wx.Button(panel, label="Install", name="ButtonInstall")
        button_install_modpack.Bind(wx.EVT_BUTTON, install_selected_modpack)

        # and create a sizer to manage the layout of child widgets
        sizer.Add(
            static_text_current_modpack_header,
            wx.SizerFlags().Border(wx.TOP | wx.LEFT | wx.RIGHT, 25),
        )
        sizer.Add(
            static_text_current_modpack_name,
            wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 25),
        )

        sizer.Add(
            button_uninstall_current_modpack,
            wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 25),
        )

        sizer.Add(
            static_text_configuration_header,
            wx.SizerFlags().Border(wx.TOP | wx.LEFT | wx.RIGHT, 25),
        )
        sizer.Add(
            static_text_hades_folder,
            wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 25),
        )
        sizer.Add(
            folder_picker_hades_folder,
            wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 25),
        )
        sizer.Add(
            static_text_modpack_folder,
            wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 25),
        )
        sizer.Add(
            folder_picker_modpack_folder,
            wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 25),
        )

        sizer.Add(
            static_text_choose_modpack_header,
            wx.SizerFlags().Border(wx.TOP | wx.LEFT | wx.RIGHT, 25),
        )
        sizer.Add(
            combo_box_choose_modpack,
            wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 25),
        )
        sizer.Add(
            button_install_modpack,
            wx.SizerFlags().Border(wx.LEFT | wx.BOTTOM | wx.RIGHT, 25),
        )

        panel.SetSizerAndFit(sizer)

    def update_hades_folder_path(self, event: wx.FileDirPickerEvent):
        config["HADES"]["PATH"] = event.GetPath()
        logging.debug(f"Updating hades folder to: {config['HADES']['PATH']}")
        with open("config.ini", "w") as config_file:
            config.write(config_file)

    def update_modpack_folder_path(self, event: wx.FileDirPickerEvent):
        config["MODPACKS"]["PATH"] = event.GetPath()
        logging.debug(f"Updating modpack folder to: {config['MODPACKS']['PATH']}")
        with open("config.ini", "w") as config_file:
            config.write(config_file)

    def update_selected_modpack(self, event: wx.CommandEvent):
        modpack_name = event.GetString()

        modpack_folder_path = config["MODPACKS"]["PATH"]
        if not modpack_folder_path:
            raise PathNotSelected()

        modpack_path = Path(modpack_folder_path) / f"{modpack_name}.zip"
        modpack_path = modpack_path.resolve()

        config["MODPACKS"]["SELECTED"] = str(modpack_path)
        with open("config.ini", "w") as config_file:
            config.write(config_file)


def get_combo_box_choose_modpack(panel, config):
    modpack_path = Path(config["MODPACKS"]["PATH"])
    list_of_modpacks = available_modpacks(modpack_path)

    return wx.ComboBox(
        panel,
        choices=list_of_modpacks,
        name="ComboBoxChooseModpack",
    )
