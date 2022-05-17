
def bar_listener(song, on_bar):
    def callback():
        beat_time = song().get_current_beats_song_time() 
        if beat_time.beats == 1:
            on_bar(beat_time.bars)
    song().add_current_song_time_listener(callback)        