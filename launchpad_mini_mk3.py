#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Mini_MK3/launchpad_mini_mk3.py
# from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement, Color
from _Framework.Skin import Skin
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.SysexValueControl import SysexValueControl

from .PadLight import PadLight
from .MyButton import MyButton


# https://forum.ableton.com/viewtopic.php?f=1&t=200513&start=0
# Live API - https://structure-void.com/PythonLiveAPI_documentation/Live10.0.1.xml

class Colors:
    RED    = Color(5)
    GREEN  = Color(21)
    YELLOW = Color(13)

class Buttons: 
    STOP = Colors.RED
    PLAY = Colors.GREEN
    BEAT = Colors.RED
    CLICK = Colors.YELLOW
    SONG0 = Color(53)
    SONG1 = Color(79)
    SONG2 = Color(87)
    SONG3 = Color(36)
    SONG4 = Color(69)
    SONG5 = Color(9)
    SONG6 = Color(74)
    SONG7 = Color(2)

SONG_COLORS = [
    Color(53),
    Color(79),
    Color(87),
    Color(36),
    Color(69),
    Color(9),
    Color(74),
    Color(2)
]

class Launchpad_Mini_MK3(ControlSurface):

    def __init__(self, c_instance):                #initialize the sparkLE2 class as a ControleSurface
        super(Launchpad_Mini_MK3, self).__init__(c_instance, False)
        with self.component_guard():
            self.log_message('Chris Launchpad Mini Initializing...')
            self._set_programmer_mode()
            self._create_components()
            self._setup_listeners()
            self.show_message('Chris Launchpad Mini Initialized!')
            self.log_message('Chris Launchpad Mini Initialized!')

    def _set_programmer_mode(self):
        sysex = SysexValueControl((240, 0, 32, 41, 2, 13, 14))
        sysex.send_value((1,))

    def _setup_listeners(self): 
        self._setup_beat_tracker()

    def _setup_beat_tracker(self):     
        self.song().add_current_song_time_listener(self.song_listener)
        self._beat_button = MyButton(99, Colors.RED, start_on = False)

        self._beat_top_matrix = [0]*8
        for i in range(8):
            self._beat_top_matrix[i] = MyButton(81 + i, Colors.RED, start_on = False)

    def song_listener(self): 
        beat_time = self.song().get_current_beats_song_time() 
        tup = (beat_time.beats, beat_time.sub_division)
        if tup != self._last_seen:
            self._last_seen = tup
            self.beat_listener(tup[0], tup[1])

    def beat_listener(self, beat, div):        
        self._metronome_led_listener(beat, div)
        self._metronome_row_listener(beat, div)

    def _metronome_row_listener(self, beat, div):
        if div == 1:
            self._beat_top_matrix[beat - 1].solid(Colors.GREEN if beat == 1 else Colors.RED)
            if self._last_top != None:
                self._beat_top_matrix[self._last_top].off()    
            self._last_top = beat - 1

    def _metronome_led_listener(self, beat, div): 
        if div == 1:
            self._beat_button.solid(Colors.GREEN if beat == 1 else Colors.RED)
        elif div == 3:
            self._beat_button.off()  

    def _create_components(self):
        self._create_play_stop()
        self._create_song_buttons()
        self._create_click_button()

    def _create_click_button(self):
        self._click_button = MyButton(89, Colors.YELLOW, self._click_pressed)

    def _click_pressed(self):
        self.song().metronome = not self.song().metronome

    def _create_play_stop(self):
        self._stop_button = MyButton(19, Colors.RED, self._stop_pressed)
        self._play_button = MyButton(29, Colors.GREEN, self._play_pressed)

    def _create_song_buttons(self):
        for i in range(8):
            MyButton(11 + i, SONG_COLORS[i])    

    def _stop_pressed(self):
        self.song().stop_playing()
        self._beat_button.off()
        self._beat_top_matrix[self._last_top].off()            

    def _play_pressed(self):
        self._last_seen = (0, 0)   
        self._last_top = None
        self.song().start_playing()
