import logging

from .MyButton import MyButton
from .Color import Color, Colors

LOOPS_TRACK_NAME = 'Loops'
LOOP_BUTTONS_START = 41

class LoopClips:

    def __init__(self, song):
        self._song = song
        self._loop_clips = self._get_loop_clips(song)
        self._clip_ptr_dict = {}
        self._create_buttons()
        self._active_loops = []

    def add_clip(self, clip):
        self._clip_ptr_dict[str(clip._live_ptr)] = self._get_loop_clips_in_clip(clip) 

    def activate_clip(self, clip):
        self._clear_buttons()
        loops = self._clip_ptr_dict.get(str(clip._live_ptr), None)
        if loops is not None:
            for index in range(min(len(loops),8)):
                loop_clip = loops[index]
                self._buttons[index].solid(Color(loop_clip.color, is_rgb=True))
            self._active_loops = loops    

    def _clear_buttons(self):
        for button in self._buttons:
            button.off()

    def _create_buttons(self):
        self._buttons = []
        for i in range(8):
            self._buttons.append(
                MyButton(
                    address = LOOP_BUTTONS_START + i,
                    color = Colors.GREEN,
                    on_click=self._on_loop_click(i),
                    start_on = False
                )
            )              

    def _on_loop_click(self, i):
        def func():
            if i < len(self._active_loops):
                clip = self._active_loops[i]
                self._song().loop_start = clip.start_time
                self._song().loop_length = clip.end_time - clip.start_time
        return func

    def _get_loop_clips(self, song):
        clips = []
        for track in song().tracks:
            if track.name == LOOPS_TRACK_NAME:
                clips = track.arrangement_clips
        return clips        
    
    def _get_loop_clips_in_clip(self, clip):
        clips = []
        for loop_clip in self._loop_clips:
            if loop_clip.start_time >= clip.start_time and loop_clip.end_time <= clip.end_time:
                clips.append(loop_clip)
        return clips