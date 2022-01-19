import wx
from gui.select_modpack import SelectModpackFrame

app = wx.App()

frame = SelectModpackFrame(None, title="Hades Modpack Manager")

frame.Fit()
frame.Show()

app.MainLoop()
