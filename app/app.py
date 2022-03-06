from wx import App

from gui.select_modpack import SelectModpackFrame


app = App()

frame = SelectModpackFrame(None, title="Hades Modpack Manager")
frame.Fit()
frame.Show()

app.MainLoop()
