import wx
import pygame


def bitmap_button_creation(path, width, height, parent, position_x, position_y, toggle=False):
    bitmap = wx.Bitmap(path)
    image = bitmap.ConvertToImage()
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.Bitmap(image)
    if not toggle:
        button_created = wx.BitmapButton(parent, pos=(position_x, position_y), size=(height, width), bitmap=result)

    else:
        button_created = wx.BitmapToggleButton(parent, pos=(position_x, position_y), size=(height, width), label=result)
    return button_created


class NewFrame(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title='test', size=(800, 300))
        panel = wx.Panel(self)
        new_button = wx.ToggleButton(panel, pos=(10, 10), size=(100, 100), label='click me')
        new_button.Bind(wx.EVT_TOGGLEBUTTON, self.onClick)
        pygame.mixer.init()
        pygame.mixer.music.load('shewants.mp3')
        self.is_paused = False
        self.Show()

    def onClick(self, event):
        btn_var = event.GetEventObject().GetValue()
        if btn_var:
            pygame.mixer.music.play()
        else:
            pygame.mixer.stop()


app = wx.App()
frame = NewFrame()
app.MainLoop()