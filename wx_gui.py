# TODO:
# - clock:
#   - how many seconds since the track started playing
#   - how many seconds left
#   - self.clock = pygame.time.Clock()

# TODO:
# - integration with DirDialog (lines 157-169)

# TODO:
# - assign the value of working_directory to the folder above
# - change the label on the UI
# - *perhaps* add a playlist feature - an additional part of the UI with the .mp3 files listed

# icons used are from icons8.com for the code to work you will need three bitmaps which will be assigned to icons,
# as well as .mp3 files located in the same catalog as your .py code

import wx
import pygame
import os
import random
from mutagen.mp3 import MP3



# wx Frame
class MyFrame(wx.Frame):
    def __init__(self):
        ### wx shit goes here ###

        super().__init__(parent=None, title='MP3 Player', size=(800, 300))
        panel = wx.Panel(self)

        # PYGAME INITIATION (lines 39-52)
        self.playlist = []
        self.pygame_mixer_initiation()

        # UI CREATION (lines 55-86)
        self.UI_elements_creation(panel)

        #timer
        # self.timer = wx.Timer(self)
        # self.Bind(wx.EVT_TIMER, self.OnTimer)
        # self.timer.Start(1000)  # 1 second interval


    # PYGAME MIXER
    def pygame_mixer_initiation(self):
        ### pygame shit goes here
        # where the music will be playing from
        pygame.mixer.init()
        self.folder = '~/Desktop/moje_projektowe/' # <- PATH TO THE PROJECT CATALOG


        # playlist creation for playback
        self.playlist_creation(self.folder)

        # index needed to navigate through the playlist
        self.i = 0

        # initiation of pygame mixer
        pygame.mixer.music.load(self.playlist[self.i])


    # UI CREATION
    def UI_elements_creation(self, panel):
        # BG COLOR
        self.SetBackgroundColour('#ffffff')

        # LEFT SIDE WITH LABELS

        self.playing_from_label = label_creation(panel, 'NOW PLAYING FROM', 13, 99, 54, '#707070')

        self.label = self.folder.split('/')[-2]
        self.user_whereabouts_label = label_creation(panel, self.label, 17, 99, 79, '#FF2D55')

        self.song_title_label = label_creation(panel, 'Song Title', 22, 99, 123, '#000000', 'bold')
        self.artist_label = label_creation(panel, 'Artist Name', 17, 99, 157, '#707070')

        self.time_from_beginning_label = label_creation(panel, '0:00', 11, 99, 217, '#FF2D55')
        self.song_length_label = label_creation(panel, '21:37', 11, 391, 217, '#FF2D55')

        # RIGHT SIDE WITH BUTTONS
        self.change_folder_button = wx.Button(panel, label='CHANGE FOLDER', pos=(510, 54), size=(183, 36))
        self.change_folder_button.Bind(wx.EVT_BUTTON, self.change_folder_button_clicked)

        self.backward_button = bitmap_button_creation('icon_backward.png', 40, 40, panel, 510, 130)
        self.backward_button.Bind(wx.EVT_BUTTON, self.backward_button_clicked)

        self.play_button = bitmap_button_creation('icon_play.png', 80, 80, panel, 560, 110, toggle=True)
        self.play_button.Bind(wx.EVT_TOGGLEBUTTON, self.play_button_clicked)

        self.forward_button = bitmap_button_creation('icon_forward.png', 40, 40, panel, 650, 130)
        self.forward_button.Bind(wx.EVT_BUTTON, self.forward_button_clicked)

        self.shuffle_button = bitmap_button_creation('icon-shuffle.png', 30, 30, panel, 585, 200, toggle=True)
        self.shuffle_button.Bind(wx.EVT_TOGGLEBUTTON, self.shuffle_button_clicked)

        # SHOWING UI ELEMENTS
        self.Show()

    # BUTTON ACTIONS
    def play_button_clicked(self, event):
        # this returns a bool
        self.btn_var = event.GetEventObject().GetValue()
        # for the toggle button to pause/unpause
        if pygame.mixer.music.get_busy():
            if self.btn_var:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
        # this part is needed to *start* playback when pygame mixer is not busy,
        # so it's only used ONCE
        else:
            if self.btn_var:
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.pause()

        self.update_track_label()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(1000)  # 1 second interval


    def forward_button_clicked(self, event):
        self.time_from_beginning_label.SetLabel('0:00')
        # in case playback has been stopped, this feature is parallel to the rest of
        # music players: if you click forward, music starts playing
        self.play_button.SetValue(1)
        self.i += 1
        # this allows for moving through the playlist - modulo operation returns the
        # index of the track to be played
        pygame.mixer.music.load(self.playlist[self.i % len(self.playlist)])
        self.update_track_label()
        # print('obecne i:', self.i % len(self.playlist))
        pygame.mixer.music.play()

    def backward_button_clicked(self, event):
        self.time_from_beginning_label.SetLabel('0:00')
        self.play_button.SetValue(1)
        self.i -= 1
        pygame.mixer.music.load(self.playlist[self.i % len(self.playlist)])
        # print('obecne i:', self.i % len(self.playlist))
        self.update_track_label()
        pygame.mixer.music.play()
        self.onTimer()

    def change_folder_button_clicked(self, event):
        # changes music source, NOT DONE YET
        # CODE SOURCE: (http://www.java2s.com/Tutorial/Python/0380__wxPython/ChooseadirectoryfromDirDialog.htm)

        self.dialog = wx.DirDialog(None, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if self.dialog.ShowModal() == wx.ID_OK:
            folder = self.dialog.GetPath() + '/'
            print(folder)
            # TUTAJ COŚ NIE DZIAŁA XD
            self.playlist = self.playlist_creation(folder)
            print(self.playlist)
        self.dialog.Destroy()


    def shuffle_button_clicked(self, event):
        self.shuffle_var = event.GetEventObject().GetValue()
        if self.shuffle_var:
            self.playlist = self.playlist_creation(self.folder, shuffle_var=True)
        else:
            self.playlist = self.playlist_creation(self.folder)


    def update_track_label(self):
        self.song_title_label.SetLabel(self.playlist[self.i % len(self.playlist)])

    def OnTimer(self, event):
        while self.btn_var:
            timer_value = self.time_from_beginning_label.GetLabel()
            # print('timer value: ' + str(timer_value))
            timer_value_split = timer_value.split(':')
            # print('timer value split:' + str(timer_value.split(':')))

            minutes = int(timer_value_split[0])
            seconds = int(timer_value_split[-1])

            timer_value = minutes * 60 + seconds
            # print('timer value intowe: ' + str(timer_value))
            # timer_value = int(timer_value)
            timer_value += 1

            if timer_value < 10:
                minutes = 0
                seconds = timer_value
                new_value = '0:0' + str(seconds)
            elif 10 <= timer_value < 60:
                minutes = 0
                seconds = timer_value % 60
                new_value = str(minutes) + ':' + str(timer_value)
            else:
                minutes = timer_value // 60
                seconds = timer_value % 60
                if seconds < 10:
                    new_value = str(minutes) + ':0' + str(seconds)
                else:
                    new_value = str(minutes) + ':' + str(seconds)

            self.time_from_beginning_label.SetLabel(new_value)
            break

    def playlist_creation(self, path, shuffle_var=False):
        self.playlist = []
        if not shuffle_var:
            for filename in os.listdir(os.path.expanduser(path)):
                if filename.endswith('.mp3'):
                    self.playlist.append(filename)
            print(self.playlist)
        else:
            random.shuffle(self.playlist)
            print(self.playlist)
        return self.playlist


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


# playlist creation method
# def playlist_creation(path, playlist=[], shuffle_var=False):
#     if not shuffle_var:
#         for filename in os.listdir(os.path.expanduser(path)):
#             if filename.endswith('.mp3'):
#                 playlist.append(filename)
#         print(playlist)
#     else:
#         random.shuffle(playlist)
#         print(playlist)
#     return playlist


# a function which runs the program
def main():
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()


main()



