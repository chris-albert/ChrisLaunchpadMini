

class Color(object):

    def __init__(self, midi_value, is_rgb = False, *a, **k):
        super(Color, self).__init__(*a, **k)
        self.midi_value = midi_value
        self.is_rgb = is_rgb