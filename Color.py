
class Color(object):

    def __init__(self, midi_value, is_rgb = False, *a, **k):
        super(Color, self).__init__(*a, **k)
        self.midi_value = midi_value
        self.is_rgb = is_rgb


class Colors:
    RED    = Color(5)
    GREEN  = Color(21)
    YELLOW = Color(13)
    LIGHT_BLUE = Color(37)
    DARK_BLUE = Color(45)
    PINK = Color(95)
    BROWN = Color(127)
    BLACK = Color(0)      