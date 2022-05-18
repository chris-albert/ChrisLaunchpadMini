import logging
from .MyButton import MyButton
from .Color import Color, Colors
from .TrackClipListener import TrackClipListener

PARTS_TRACK_NAME = 'Parts'
PARTS_BUTTON_START = 41

class PartsTracker:

    def __init__(self, song, bar_listener):
        self._parts_clips = self._get_parts_clips(song)
        self._setup_clip_listener(self._parts_clips, bar_listener)
        self._create_buttons()
        self._clip_ptr_dict = {}
        self._active_parts = []

        self._clip_ptr_stack = None


    def add_clip(self, clip):
        clip_parts = self._get_part_clips_in_clip(clip) 
        self._clip_ptr_dict[str(clip._live_ptr)] = clip_parts
        

    def activate_song_clip(self, clip):
        self._clear_buttons()
        self._active_parts = self._clip_ptr_dict.get(str(clip._live_ptr), [])
        self._clip_ptr_stack = ClipPtrStack(self._active_parts)
        self._render_buttons(self._clip_ptr_stack.get_color_arr())

    def _setup_clip_listener(self, part_clips, bar_listener):
        track_clip_listener = TrackClipListener(bar_listener)
        for index in range(len(part_clips)):
            part_clip = part_clips[index]
            track_clip_listener.on_clip_change(part_clip, self._on_clip_change)
    
    def _on_clip_change(self, clip, bar, active):
        if self._clip_ptr_stack is not None:
            self._update_buttons(clip, active)   

    def _update_buttons(self, clip, active):
        if active:
            self._clip_ptr_stack.clip_enter(clip)
            # logging.info("Enter part clip [{}]".format(clip.name))
        else:
            self._clip_ptr_stack.clip_exit(clip)   
            # logging.info("Exit part clip [{}]".format(clip.name))

        self._render_buttons(self._clip_ptr_stack.get_color_arr())  

    def _render_buttons(self, color_arr):
        self._clear_buttons()
        for index in range(len(color_arr)):
            color = color_arr[index]
            self._buttons[index].set_color(color)
            self._buttons[index].solid()

    def _create_buttons(self):
        self._buttons = []
        for i in range(8):
            self._buttons.append(
                MyButton(
                    address = PARTS_BUTTON_START + i,
                    color = Colors.GREEN,
                    start_on = False
                )
            )          

    def _clear_buttons(self):
        for button in self._buttons:
            button.off()        

    def _get_parts_clips(self, song):
        clips = []
        for track in song().tracks:
            if track.name == PARTS_TRACK_NAME:
                clips = track.arrangement_clips
        return clips

    def _get_part_clips_in_clip(self, clip):
        clips = []
        for loop_clip in self._parts_clips:
            if loop_clip.start_time >= clip.start_time and loop_clip.end_time <= clip.end_time:
                clips.append(loop_clip)
        return clips

class ClipPtrStack:

    def __init__(self, clips):
        self._clips = clips      
        self._clip_ptr_index = {} 
        for index in range(len(clips)):
            clip = clips[index]
            self._clip_ptr_index[str(clip._live_ptr)] = index
        self._current_index = 0

    def clip_exit(self, clip):
        # logging.info("Exiting index [{}]".format(self._clip_ptr_index.get(str(clip._live_ptr), None)))
        exiting_index = self._clip_ptr_index.get(str(clip._live_ptr), None)
        if exiting_index is not None and exiting_index + 1 >= len(self._clips):
            self._current_index = None

    def clip_enter(self, clip):
        # logging.info("Entering index [{}]".format(self._clip_ptr_index.get(str(clip._live_ptr), None)))
        entered_index = self._clip_ptr_index.get(str(clip._live_ptr), None)
        if entered_index is not None:
            self._current_index = entered_index

    def get_color_arr(self):
        if self._current_index is None:
            return []
        else:
            arr = self._clips[slice(self._current_index, self._current_index + 8)]
            return list(map(lambda clip: Color(clip.color, is_rgb=True), arr))
