# icons used are from icons8.com
# for the code to work you will need three bitmaps which can be downloaded from github catalog

import wx
import pygame
import os


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


def label_creation(parent, user_text, fontsize, position_x, position_y, color, weight=False):
    label_created = wx.StaticText(parent, style=wx.ALIGN_CENTER, pos=(position_x, position_y))
    label_text = str(user_text)
    if not weight:
        label_weight = wx.NORMAL
    elif weight == "bold":
        label_weight = wx.BOLD
    elif weight == "light":
        label_weight = wx.LIGHT
    font = wx.Font(int(fontsize), wx.SWISS, wx.NORMAL, label_weight)
    label_created.SetForegroundColour(color)
    label_created.SetFont(font)
    label_created.SetLabel(label_text)
    return label_created


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='MP3 Player', size=(800, 300))
        panel = wx.Panel(self)
        pygame.mixer.init()

        folder = '~/Desktop/project_files'

        self.i = 0

        self.playlist = []
        for filename in os.listdir(os.path.expanduser(folder)):
            if filename.endswith('.mp3'):
                self.playlist.append(filename)
        for i in range(len(self.playlist)):
            print(i, self.playlist[i])

        pygame.mixer.music.load(self.playlist[self.i])

        self.SetBackgroundColour('#ffffff')

        # LEFT SIDE WITH LABELS

        playing_from_label = label_creation(panel, 'NOW PLAYING FROM', 13, 99, 54, '#707070')
        user_whereabouts_label = label_creation(panel, 'Twoja Stara in Desktop', 17, 99, 79, '#FF2D55')

        song_title_label = label_creation(panel, 'Song Title', 22, 99, 123, '#000000', 'bold')
        artist_label = label_creation(panel, 'Artist Name', 17, 99, 157, '#707070')

        time_from_beginning_label = label_creation(panel, '06:15', 11, 99, 217, '#FF2D55')
        song_length_label = label_creation(panel, '21:37', 11, 391, 217, '#FF2D55')

        # --------------------------------------

        # RIGHT SIDE WITH BUTTONS

        change_folder_button = wx.Button(panel, label='CHANGE FOLDER', pos=(510, 54), size=(183, 36))

        backward_button = bitmap_button_creation('icon_backward.png', 40, 40, panel, 510, 130)
        backward_button.Bind(wx.EVT_BUTTON, self.backward_button_clicked)

        # event binding for toggle button
        play_button = bitmap_button_creation('icon_play.png', 80, 80, panel, 560, 110, toggle=True)
        play_button.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_button_clicked)

        forward_button = bitmap_button_creation('icon_forward.png', 40, 40, panel, 650, 130)
        forward_button.Bind(wx.EVT_BUTTON, self.forward_button_clicked)
        # --------------------------------------

        self.Show()

    def toggle_button_clicked(self, event):
        btn_var = event.GetEventObject().GetValue()
        if btn_var:
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.stop()

    def forward_button_clicked(self, event):
        self.i += 1
        pygame.mixer.music.load(self.playlist[self.i % len(self.playlist)])
        print('obecne i:', self.i % len(self.playlist))
        pygame.mixer.music.play()

    def backward_button_clicked(self, event):
        self.i -= 1
        pygame.mixer.music.load(self.playlist[self.i % len(self.playlist)])
        print('obecne i:', self.i % len(self.playlist))
        pygame.mixer.music.play()


app = wx.App()
frame = MyFrame()
app.MainLoop()