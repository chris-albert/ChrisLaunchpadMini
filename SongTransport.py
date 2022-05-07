import logging
from .MyButton import MyButton
from .Color import Color

SONGS_TRACK_NAME = 'Songs'
SONG_BUTTONS_START = 11

class SongTransport:

    def __init__(self, songFunction):
        self._song = songFunction
        self._parse_tracks()

    def _parse_tracks(self):
        for track in self._song().tracks:      
            if track.name == SONGS_TRACK_NAME:
                self._parse_songs_track(track)

    def _parse_songs_track(self, track):
        clips = self._get_sorted_clips(track)
        clipsLen = len(clips)

        self._song_buttons = [0] * min(clipsLen, 8)
        
        for i in range(len(self._song_buttons)):
            clip = clips[i]['clip']
            self._song_buttons[i] = MyButton(SONG_BUTTONS_START + i, Color(clip.color, is_rgb=True), self._song_pressed(clip, i))

    def _song_pressed(self, clip, index):
        def func():
            self._song().current_song_time = clip.start_time
            for i in range(len(self._song_buttons)):
                if i == index:
                    self._song_buttons[i].pulse()
                else:
                    self._song_buttons[i].solid()    
            
        return func

    def _get_sorted_clips(self, track):
        clipsLen = len(track.arrangement_clips)
        arr = []
        for i in range(clipsLen):
            clip = track.arrangement_clips[i]
            arr.append({
                'clip' : clip,
                'index': i
            })
        arr.sort(key = lambda e: e['clip'].name)
        return arr   