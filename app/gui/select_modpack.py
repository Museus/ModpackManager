from pathlib import Path

import wx

from config import config
from util import (
    get_current_modpack,
    get_list_of_modpacks,
    install_selected_modpack,
    uninstall_mods,
    update_hades_folder_path,
    update_modpack_folder_path,
    update_selected_modpack,
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
        unverified_modimporter_tex = wx.StaticText(
            panel, label="Warning: This manager does not verify modimporter.py"
        )
        font = unverified_modimporter_tex.GetFont()
        font = font.Bold()
        unverified_modimporter_tex.SetFont(font)

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
            get_current_modpack(Path(config["HADES"]["path"]))
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
            wx.EVT_DIRPICKER_CHANGED, update_hades_folder_path
        )

        static_text_modpack_folder = wx.StaticText(
            panel, label="Modpack Folder", name="ModpackFolderStaticText"
        )
        folder_picker_modpack_folder = wx.DirPickerCtrl(
            panel, path=config["MODPACKS"]["PATH"], name="ModpackFolderPicker"
        )
        folder_picker_modpack_folder.Bind(
            wx.EVT_DIRPICKER_CHANGED, update_modpack_folder_path
        )

        static_text_choose_modpack_header = wx.StaticText(
            panel, label="Modpack to Install"
        )
        font = static_text_choose_modpack_header.GetFont()
        font.PointSize += 5
        font = font.Bold()
        static_text_choose_modpack_header.SetFont(font)

        combo_box_choose_modpack = get_combo_box_choose_modpack(panel, config)
        combo_box_choose_modpack.Bind(wx.EVT_COMBOBOX, update_selected_modpack)

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


def get_combo_box_choose_modpack(panel, config):
    modpack_path = Path(config["MODPACKS"]["PATH"])
    list_of_modpacks = get_list_of_modpacks(modpack_path)

    return wx.ComboBox(
        panel,
        choices=list_of_modpacks,
        name="ComboBoxChooseModpack",
    )
