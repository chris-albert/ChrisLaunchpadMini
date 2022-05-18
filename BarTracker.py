import logging

from .MyButton import MyButton
from .Color import Colors, Color
from .BarListener import BarListener
from .TrackClipListener import TrackClipListener

BAR_TRACK_NAME = 'Bars'
BAR_BUTTONS_START = 51

class BarTracker:

    def __init__(self, song, bar_listener):
        
        self._current_bar = None
        self._current_count = None
        self._current_clip = None
        self._create_buttons()
        bar_clips = self._get_bar_clips(song)
        self._setup_clip_listener(bar_clips, bar_listener)
        bar_listener.add_bar_listener(self._on_bar_change)

    def _setup_clip_listener(self, bar_clips, bar_listener):
        self._clip_listener = TrackClipListener(bar_listener)
        for bar_clip in bar_clips:
            self._clip_listener.on_clip_change(bar_clip, self._on_clip_change)

    def _on_clip_change(self, clip, bar, active):
        if active:
            self._on_clip_enter(clip)
        else:
            self._on_clip_exit(clip)

    def _create_buttons(self):
        self._buttons = []
        for i in range(8):
            self._buttons.append(MyButton(BAR_BUTTONS_START + i, Colors.GREEN, start_on = False))    

    def _on_bar_change(self, bar, time):
        if self._current_bar is not None and self._current_count is not None and self._current_clip:
            if self._current_bar == 0:
                self._clear_row()
            self._buttons[self._current_bar].solid(Color(self._current_clip.color, is_rgb = True)) 
            if self._current_bar < self._current_count - 1:
                self._current_bar += 1
            else:
                self._current_bar = 0   

    def _clear_row(self):
        for button in self._buttons:
            button.off()

    def _on_clip_enter(self, clip):
        # logging.info("_on_clip_enter Name [{}] Bar [{}]".format(clip.name, clip.start_time))
        self._current_bar = 0
        self._current_count = int(clip.name)
        self._current_clip = clip
        self._clear_row()
        self._buttons[0].solid(Color(clip.color, is_rgb = True)) 

    def _on_clip_exit(self, clip):
        # logging.info("_on_clip_exit [{}] [{}]".format(clip.name, clip._live_ptr))
        if clip._live_ptr == self._current_clip._live_ptr:
            self._current_bar = None
            self._current_count = None
            self._current_clip = None
            self._clear_row()

    def _get_bar_clips(self, song):
        clips = []
        for track in song().tracks:      
            if track.name == BAR_TRACK_NAME:
                for clip in track.arrangement_clips:
                    try:
                        num = int(clip.name)
                        if num <= 8 and num > 0:
                            clips.append(clip)
                    except:
                        pass
        return clips
