import logging
from .MyButton import MyButton
from .Color import Color
from .TrackClipListener import TrackClipListener

SONGS_TRACK_NAME = 'Songs'
SONG_BUTTONS_START = 11

class SongTransport:

    def __init__(self, song, bar_listener):
        self._song = song
        cue_clips = self._get_cue_clips()
        self._create_cue_clip_buttons(cue_clips)
        self._setup_clip_listener(cue_clips, bar_listener)

    def _setup_clip_listener(self, cue_clips, bar_listener):
        track_clip_listener = TrackClipListener(bar_listener)
        for cue_clip in cue_clips:
            track_clip_listener.on_clip_change(cue_clip['clip'], self._on_clip_change(cue_clip['button']))

    def _on_clip_change(self, button):
        def func(clip, bar, active):
            if active:
                button.flash()
            else:
                button.solid()
        return func     

    def _get_cue_clips(self):
        cue_points = self._song().cue_points    
        
        cue_dict = {}
        for i in range(len(cue_points)):
            cue_point = cue_points[i]
            cue_dict[cue_point.time] = cue_point

        cue_clips = []
        for clip in self._get_song_clips():
            cue = cue_dict.get(clip.start_time, None)
            if cue is not None:
                cue_clips.append({
                    'name': clip.name,
                    'time': clip.start_time,
                    'clip': clip,
                    'cue' : cue
                })
        return cue_clips

    def _create_cue_clip_buttons(self, cue_clips):
        index = 0
        for cue_clip in cue_clips:
            button = MyButton(
                address  = SONG_BUTTONS_START + index, 
                color    = Color(cue_clip['clip'].color, is_rgb=True), 
                on_click = self._song_pressed(cue_clip)
            )
            cue_clip['button'] = button
            index += 1

    def _song_pressed(self, cue_clip):
        def func():
            cue_clip['cue'].jump()
        return func

    def _get_song_clips(self):
        clips = []
        for track in self._song().tracks:      
            if track.name == SONGS_TRACK_NAME:
                clips = self._get_sorted_clips(track)
        return clips

    def _get_sorted_clips(self, track):
        clips = []
        for c in track.arrangement_clips:
            clips.append(c)
        clips.sort(key = lambda c: c.name)
        return clips
