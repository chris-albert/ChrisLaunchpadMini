import logging
from .MyButton import MyButton
from .Color import Color

SONGS_TRACK_NAME = 'Songs'
SONG_BUTTONS_START = 11

class SongTransport:

    def __init__(self, songFunction):
        self._song = songFunction
        cue_clips = self._get_cue_clips()
        self._create_cue_clip_buttons(cue_clips)

    def _get_cue_clips(self):
        cue_points = self._song().cue_points    
        
        cue_dict = {}
        for i in range(len(cue_points)):
            cue_point = cue_points[i]
            cue_dict[cue_point.time] = cue_point

        cue_clips = []
        for clip in self._get_song_clips():
            cue_clips.append({
                'name': clip.name,
                'time': clip.start_time,
                'clip': clip,
                'cue': cue_dict.get(clip.start_time, None)
            })
        return cue_clips

    def _create_cue_clip_buttons(self, cue_clips):
        index = 0
        self._song_buttons = []
        for cue_clip in cue_clips:
            if cue_clip['cue'] is not None:
                self._song_buttons.append(
                    MyButton(SONG_BUTTONS_START + index, Color(cue_clip['clip'].color, is_rgb=True), self._song_pressed(cue_clip, index))
                )
                index += 1

    def _song_pressed(self, cue_clip, index):
        def func():
            cue_clip['cue'].jump()
            for i in range(len(self._song_buttons)):
                if i == index:
                    self._song_buttons[i].pulse()
                else:
                    self._song_buttons[i].solid()  
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
