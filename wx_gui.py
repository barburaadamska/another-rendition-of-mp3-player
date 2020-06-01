# icons used are from icons8.com for the code to work you will need three bitmaps which will be assigned to icons,
# as well as .mp3 files located in the same catalog as your .py code

import wx
import pygame
import os
import random


# shortened button creation method
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


# shortened label creation
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

def playlist_creation(path, playlist = [], shuffle_var = False):
    if not shuffle_var:
        for filename in os.listdir(os.path.expanduser(path)):
            if filename.endswith('.mp3'):
                playlist.append(filename)
        # print(playlist)
    else:
        random.shuffle(playlist)
        # print(playlist)
    return playlist

# wx Frame
class MyFrame(wx.Frame):
    def __init__(self):
        ### wx shit goes here ###

        super().__init__(parent=None, title='MP3 Player', size=(800, 300))
        panel = wx.Panel(self)
        pygame.mixer.init()
        self.SetBackgroundColour('#ffffff')


        ### pygame shit goes here

        # TODO:
        # - clock:
        #   - how many seconds since the track started playing
        #   - how many seconds left
        # self.clock = pygame.time.Clock()

        # where the music will be playing from
        self.folder = '~/Desktop/moje_projektowe/'

        # TODO:
        # - integration with DirDialog (lines xx-xx)

        # playlist creation for playback

        self.playlist = playlist_creation(self.folder)

        # index needed to navigate through the playlist
        self.i = 0

        # initiation of pygame mixer
        pygame.mixer.music.load(self.playlist[self.i])

        ### UI ELEMENTS GO HERE ###

        # LEFT SIDE WITH LABELS

        self.playing_from_label = label_creation(panel, 'NOW PLAYING FROM', 13, 99, 54, '#707070')
        self.user_whereabouts_label = label_creation(panel, 'Twoja Stara in Desktop', 17, 99, 79, '#FF2D55')

        self.song_title_label = label_creation(panel, 'Song Title', 22, 99, 123, '#000000', 'bold')
        self.artist_label = label_creation(panel, 'Artist Name', 17, 99, 157, '#707070')

        self.time_from_beginning_label = label_creation(panel, '06:15', 11, 99, 217, '#FF2D55')
        self. song_length_label = label_creation(panel, '21:37', 11, 391, 217, '#FF2D55')

        # --------------------------------------

        # RIGHT SIDE WITH BUTTONS & EVENT BINDS

        self.change_folder_button = wx.Button(panel, label='CHANGE FOLDER', pos=(510, 54), size=(183, 36))
        self.change_folder_button.Bind(wx.EVT_BUTTON, self.change_folder_button_clicked)

        self.backward_button = bitmap_button_creation('icon_backward.png', 40, 40, panel, 510, 130)
        self.backward_button.Bind(wx.EVT_BUTTON, self.backward_button_clicked)

        # event binding for toggle button
        self.play_button = bitmap_button_creation('icon_play.png', 80, 80, panel, 560, 110, toggle=True)
        self.play_button.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_button_clicked)

        self.forward_button = bitmap_button_creation('icon_forward.png', 40, 40, panel, 650, 130)
        self.forward_button.Bind(wx.EVT_BUTTON, self.forward_button_clicked)

        self.shuffle_button = bitmap_button_creation('icon-shuffle.png', 30, 30, panel, 585, 200, toggle=True)
        self.shuffle_button.Bind(wx.EVT_TOGGLEBUTTON, self.shuffle_button_clicked)
        # --------------------------------------

        self.Show()

    def toggle_button_clicked(self, event):
        # this returns a bool
        btn_var = event.GetEventObject().GetValue()
        # for the toggle button to pause/unpause
        if pygame.mixer.music.get_busy():
            if btn_var:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
        # this part is needed to *start* playback when pygame mixer is not busy,
        # so it's only used ONCE
        else:
            if btn_var:
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.pause()

    def forward_button_clicked(self, event):
        # in case playback has been stopped, this feature is parallel to the rest of
        # music players: if you click forward, music starts playing
        self.play_button.SetValue(1)
        self.i += 1
        # this allows for moving through the playlist - modulo operation returns the
        # index of the track to be played
        pygame.mixer.music.load(self.playlist[self.i % len(self.playlist)])
        # print('obecne i:', self.i % len(self.playlist))
        pygame.mixer.music.play()

    def backward_button_clicked(self, event):
        self.play_button.SetValue(1)
        self.i -= 1
        pygame.mixer.music.load(self.playlist[self.i % len(self.playlist)])
        # print('obecne i:', self.i % len(self.playlist))
        pygame.mixer.music.play()

    def change_folder_button_clicked(self, event):
        # changes music source, NOT DONE YET
        # CODE SOURCE: (http://www.java2s.com/Tutorial/Python/0380__wxPython/ChooseadirectoryfromDirDialog.htm)

        self.dialog = wx.DirDialog(None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if self.dialog.ShowModal() == wx.ID_OK:
            self.working_directory = self.dialog.GetPath()
            # TODO:
            # - assign the value of working_directory to the folder above
            # - change the label on the UI
            # - *perhaps* add a playlist feature - an additional part of the UI with the .mp3 files listed
            print(self.dialog.GetPath())
        self.dialog.Destroy()

    def shuffle_button_clicked(self, event):
        self.shuffle_var = event.GetEventObject().GetValue()
        if self.shuffle_var:
            self.playlist = playlist_creation(self.folder, shuffle_var=True)
        else:
            self.playlist = playlist_creation(self.folder, playlist=[])


# initiation of the app
app = wx.App()
frame = MyFrame()
app.MainLoop()
