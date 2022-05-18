#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Mini_MK3/launchpad_mini_mk3.py
# from __future__ import absolute_import, print_function, unicode_literals
from re import S
from _Framework.ControlSurface import ControlSurface
from _Framework.Skin import Skin
from _Framework.InputControlElement import MIDI_NOTE_TYPE
from _Framework.SysexValueControl import SysexValueControl

from .MyButton import MyButton
from .SongTransport import SongTransport
from .BarTracker import BarTracker
from .Color import Color, Colors
from .BarListener import BarListener

class ChrisLaunchpadMini(ControlSurface):

    def __init__(self, c_instance):                #initialize the sparkLE2 class as a ControleSurface
        super(ChrisLaunchpadMini, self).__init__(c_instance, False)
        with self.component_guard():
            self.log_message('Chris Launchpad Mini Initializing...')
            self._last_top = None
            self._last_seen = None
            self._current_time_sig_numerator = 0
            self._current_time_sig_denominoator = 0
            self._set_programmer_mode()
            self._create_components()
            self._setup_listeners()
            
            self._bar_listener = BarListener(self.song)
            self._song_transport = SongTransport(self.song, self._bar_listener)
            self._bar_tracker = BarTracker(self.song, self._bar_listener)
            self.show_message('Chris Launchpad Mini Initialized!')
            self.log_message('Chris Launchpad Mini Initialized!')

    def _set_programmer_mode(self):
        sysex = SysexValueControl((240, 0, 32, 41, 2, 13, 14))
        sysex.send_value((1,))

    def _setup_listeners(self): 
        self._setup_beat_tracker()
        self.song().add_is_playing_listener(self._playing_listener)
        self.song().add_loop_listener(self._loop_listener)

    def _loop_listener(self):
        if self.song().loop:
            self._loop_button.flash()
        else:
            self._loop_button.solid()        

    def _playing_listener(self):
        if self.song().is_playing:
            self._play_button.flash()
            self._stop_button.solid()
        else:
            self._play_button.solid()
            self._stop_button.flash()

    def _setup_beat_tracker(self):     
        self.song().add_current_song_time_listener(self.song_listener)
        self._beat_button = MyButton(99, Colors.RED, start_on = False)

        self._beat_top_matrix = [0]*8
        for i in range(8):
            self._beat_top_matrix[i] = MyButton(81 + i, Colors.RED, start_on = False)

    def song_listener(self): 
        self._update_time_sig_buttons(self.song().signature_numerator, self.song().signature_denominator)
        beat_time = self.song().get_current_beats_song_time() 
        tup = (beat_time.beats, beat_time.sub_division)
        # self.log_message('Bars [{}] Beats [{}] Sub Division [{}] Ticks [{}]'.format(beat_time.bars, beat_time.beats, beat_time.sub_division, beat_time.ticks))
        if tup != self._last_seen:
            self._last_seen = tup
            self.beat_listener(tup[0], tup[1])  

    def _update_time_sig_buttons(self, numerator, denominator):
        if self._current_time_sig_numerator != numerator or self._current_time_sig_denominator == denominator:
            self._current_time_sig_numerator = numerator 
            self._current_time_sig_denominator = denominator
            for n in range(8):
                if n < numerator:
                    self._time_sig_numerator_buttons[n].solid()
                else:
                    self._time_sig_numerator_buttons[n].off()
                if n < denominator:
                    self._time_sig_denominator_buttons[n].solid()
                else:
                    self._time_sig_denominator_buttons[n].off()

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
        elif div == 2:
            self._beat_button.off()  

    def _create_components(self):
        self._create_play_stop()
        self._create_click_button()
        self._create_tempo_buttons()
        self._create_time_sig_buttons()
        self._create_loop_button()

    def _create_time_sig_buttons(self):
        self._time_sig_numerator_buttons = []
        self._time_sig_denominator_buttons = []
        for i in range(8):
            self._time_sig_numerator_buttons.append(MyButton(71 + i, Color(80), start_on = False))
            self._time_sig_denominator_buttons.append(MyButton(61 + i, Color(79), start_on = False))

    def _create_click_button(self):
        self._click_button = MyButton(89, Colors.YELLOW, self._click_pressed)

    def _click_pressed(self):
        self.song().metronome = not self.song().metronome
        if self.song().metronome:
            self._click_button.flash()
        else:
            self._click_button.solid()

    def _create_play_stop(self):
        self._stop_button = MyButton(19, Colors.RED, self._stop_pressed, start_on = False)
        self._stop_button.flash() 
        self._play_button = MyButton(29, Colors.GREEN, self._play_pressed)

    def _create_tempo_buttons(self):    
        self._tempo_up_button = MyButton(91, Colors.DARK_BLUE, self._on_tempo_up_pressed)
        self._tempo_down_button = MyButton(92, Colors.LIGHT_BLUE, self._on_tempo_down_pressed)

    def _on_tempo_up_pressed(self):    
        self.song().tempo += 1

    def _on_tempo_down_pressed(self):    
        self.song().tempo -= 1

    def _create_loop_button(self):
        self._loop_button = MyButton(39, Colors.BROWN, self._on_loop_pressed)

    def _on_loop_pressed(self):
        self.song().loop = not self.song().loop

    def _stop_pressed(self):
        self.song().stop_playing()
        self._beat_button.off()
        if self._last_top != None:
            self._beat_top_matrix[self._last_top].off()            

    def _play_pressed(self):
        self._last_seen = (0, 0)   
        self._last_top = None
        self.song().start_playing()
