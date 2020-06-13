import wx
import pygame
import os
import random


# wx Frame
class MyFrame(wx.Frame):
    def __init__(self):
        ### wx shit goes here

        super().__init__(parent=None, title='MP3 Player', size=(800, 300))
        panel = wx.Panel(self)

        # PYGAME INITIATION (lines 39-52)
        self.playlist = []
        self.pygame_mixer_initiation()

        # UI CREATION (lines 55-86)
        self.UI_elements_creation(panel)

    def pygame_mixer_initiation(self):
        ### pygame shit goes here
        # where the music will be playing from
        pygame.mixer.init()
        self.folder = os.path.dirname(os.path.abspath(__file__))

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

        self.label = self.folder.split('/')[-1]
        self.user_whereabouts_label = label_creation(panel, self.label, 17, 99, 79, '#FF2D55')

        self.song_title_label = label_creation(panel, 'Song Title', 22, 99, 123, '#000000', 'bold')
        self.artist_label = label_creation(panel, 'Artist Name', 17, 99, 157, '#707070')

        self.time_from_beginning_label = label_creation(panel, '0:00', 11, 99, 217, '#FF2D55')
        self.song_length_label = label_creation(panel, '21:37', 11, 391, 217, '#FF2D55')

        # RIGHT SIDE WITH BUTTONS

        self.backward_button = bitmap_button_creation('backward_icon.png', 40, 40, panel, 510, 130)
        self.backward_button.Bind(wx.EVT_BUTTON, self.backward_button_clicked)

        self.play_button = bitmap_button_creation('play_icon.png', 80, 80, panel, 560, 110, toggle=True)
        self.play_button.Bind(wx.EVT_TOGGLEBUTTON, self.play_button_clicked)

        self.forward_button = bitmap_button_creation('forward_icon.png', 40, 40, panel, 650, 130)
        self.forward_button.Bind(wx.EVT_BUTTON, self.forward_button_clicked)

        self.dark_mode_button = bitmap_button_creation('sun_icon.png', 20, 20, panel, 50, 50, toggle=True)
        self.dark_mode_button.Bind(wx.EVT_TOGGLEBUTTON, self.change_background_color)

        self.volume = wx.Slider(panel, 6, 5, 0, 10, (550, 200), (100, -1))
        self.volume.Bind(wx.EVT_SCROLL, self.volumeSlider, id=6)

        self.mute = bitmap_button_creation("mute_icon.png", 20, 20, panel, 530, 200, toggle=True)
        self.mute.Bind(wx.EVT_TOGGLEBUTTON, self.mute_music)
        self.mute.Bind(wx.EVT_TOGGLEBUTTON, self.change_slider_mute)

        self.about_info = bitmap_button_creation('info_icon.png', 20, 20, panel, 50, 80)
        self.about_info.Bind(wx.EVT_BUTTON, self.about_button_clicked)

        max_volume_button = bitmap_button_creation("icon_max.png", 20, 20, panel, 650, 200)
        max_volume_button.Bind(wx.EVT_BUTTON, self.maximum_volume)
        max_volume_button.Bind(wx.EVT_BUTTON, self.change_slider_max)

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

        self.update_labels()
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
        # updating labels
        self.update_labels()
        pygame.mixer.music.play()

    def backward_button_clicked(self, event):
        # sets label to 0:00
        self.time_from_beginning_label.SetLabel('0:00')
        # starts playing the song
        self.play_button.SetValue(1)
        self.i -= 1
        pygame.mixer.music.load(self.playlist[self.i % len(self.playlist)])
        self.update_labels()
        pygame.mixer.music.play()
        self.onTimer()

    # FUNCTIONS WHICH UPDATE THE UI

    def update_labels(self):
        self.song_title_label.SetLabel(self.playlist[self.i % len(self.playlist)])

    def OnTimer(self, event):
        # TIMER - time since the playback started
        while self.btn_var:
            timer_value = self.time_from_beginning_label.GetLabel()
            timer_value_split = timer_value.split(':')

            minutes = int(timer_value_split[0])
            seconds = int(timer_value_split[-1])

            timer_value = minutes * 60 + seconds
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
        # PLAYLIST CREATION FOR THE PLAYBACK
        self.playlist = []
        # this is prepared for implementation of shuffle option in next releases
        if not shuffle_var:
            for filename in os.listdir(os.path.expanduser(path)):
                if filename.endswith('.mp3'):
                    self.playlist.append(filename)
            print(self.playlist)
        else:
            random.shuffle(self.playlist)
            print(self.playlist)
        return self.playlist

    def change_background_color(self, event):
        # changes bg - DARK MODE feature
        btn = event.GetEventObject()
        if btn.GetValue():
            self.SetBackgroundColour("black")
            self.song_title_label = label_creation(self, 'Song Title', 22, 99, 123, 'white', 'bold')
            self.song_title_label.SetLabel(self.playlist[self.i % len(self.playlist)])
            self.Refresh()
        else:
            self.SetBackgroundColour("#ffffff")
            self.song_title_label = label_creation(self, 'Song Title', 22, 99, 123, '#000000', 'bold')
            self.song_title_label.SetLabel(self.playlist[self.i % len(self.playlist)])
            self.Refresh()

    def mute_music(self, event):
        # mutes curently playing song
        btn = event.GetEventObject()
        if btn.GetValue():
            vol = 0
            pygame.mixer.music.set_volume(vol)
        else:
            vol = 0.5
            pygame.mixer.music.set_volume(vol)

    def change_slider_max(self, event):
        # changes the slider position to the max
        btn = event.GetEventObject()
        self.volume.SetValue(self.volume.GetMax())
        event.Skip()

    def maximum_volume(self, event):
        # sets volume to the max
        btn = event.GetEventObject()
        new_volume = self.volume.GetMax()
        pygame.mixer.music.set_volume(new_volume)

    def volumeSlider(self, event):
        # changes the volume
        slider = event.GetEventObject()
        vol = slider.GetValue()
        vol = float(vol) / slider.GetMax()
        pygame.mixer.music.set_volume(vol)

    def change_slider_mute(self, event):
        # mutes the playback
        btn = event.GetEventObject()
        if btn.GetValue():
            self.volume.SetValue(0)
            event.Skip()
        else:
            self.volume.SetValue(int(50 / self.volume.GetMax()))
            event.Skip()

    def about_button_clicked(self, event):
        btn = event.GetEventObject()
        if btn:
            wx.MessageBox(
                "This project was created by Weronika Kozłowska, Zuzanna Kurowska, Julia Słowicka and Barbara Adamska.\n\nIcons are from https://icons8.com.",
                "About", style=wx.OK)


def bitmap_button_creation(path, width, height, parent, position_x, position_y, toggle=False):
    # shortened button creation method
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
    # shortened label creation
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


def main():
    # a function which runs the program
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()


main()