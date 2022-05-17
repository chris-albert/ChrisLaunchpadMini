
class BarListener:

    def __init__(self, song):
        self._current_bar = 0
        self._song = song
        self._song().add_current_song_time_listener(self._song_time_listener)
        self._on_bar_listeners = []

    def add_bar_listener(self, bar_listener):
        self._on_bar_listeners.append(bar_listener)

    def _song_time_listener(self):
        beat_time = self._song().get_current_beats_song_time() 
        if beat_time.beats == 1:
            if self._current_bar != beat_time.bars:
                self._current_bar = beat_time.bars
                for listener in self._on_bar_listeners:
                    listener(beat_time.bars, int(self._song().current_song_time))