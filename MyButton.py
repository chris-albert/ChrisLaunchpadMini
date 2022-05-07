from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import InputControlElement, MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_SYSEX_TYPE
from _Framework.SysexValueControl import SysexValueControl
from novation.colors import CLIP_COLOR_TABLE, RGB_COLOR_TABLE
import logging
LAUNCHPAD_SYSEX_PREFIX = (240, 0, 32, 41, 2, 13)
LIGHT_SYSEX_PREFIX = LAUNCHPAD_SYSEX_PREFIX + (3,)

SOLID_TYPE    = 0
FLASHING_TYPE = 1
PULSING_TYPE  = 2
RGB_TYPE      = 3

# I copied this from novation.util
def get_midi_color_value_for_track(midi_value):

    color = CLIP_COLOR_TABLE.get(midi_value, None)
    if color is None:
        color = find_nearest_color(RGB_COLOR_TABLE, midi_value)
    return color

# Then i copied this from ableton.v2.control_surface.components
def find_nearest_color(rgb_table, src_hex_color):

    def hex_to_channels(color_in_hex):
        return ((color_in_hex & 16711680) >> 16, (color_in_hex & 65280) >> 8, color_in_hex & 255)

    def squared_distance(color):
        return sum([ (a - b) ** 2 for a, b in zip(hex_to_channels(src_hex_color), hex_to_channels(color[1])) ])

    return min(rgb_table, key=squared_distance)[0]

def is_cc_type(address):
    address_str = str(address)
    return address_str.startswith("9") or address_str.endswith("9")

class MyButton(ButtonElement):

    def __init__(self, address, color = None, on_click = None, start_on = True):
      super(MyButton, self).__init__(
          False, 
          MIDI_CC_TYPE if is_cc_type(address) else MIDI_NOTE_TYPE, 
          0, 
          address
      )
      self._sysex = SysexValueControl(LIGHT_SYSEX_PREFIX)
      self._color = color
      self._address = address
      self._on_click = on_click
      if start_on:
          self.solid()
      if on_click != None:
          self.add_value_listener(self._value_listener)
          
    def _value_listener(self, value):
        if value == 127:
            self._on_click()

    def solid(self, color = None):
        self.send_value(self._get_color(color), True) 

    def flash(self, color = None):
        self._sysex.send_value((FLASHING_TYPE, self._address, self._get_color(color), 0))  

    def pulse(self, color = None):
        self._sysex.send_value((PULSING_TYPE, self._address, self._get_color(color)))   

    def off(self):
        self.send_value(0, True)

    def _get_color(self, color = None):
        _color = color if color != None else self._color
        if _color.is_rgb:
            return get_midi_color_value_for_track(_color.midi_value)
        else:
            return _color.midi_value

    def reset(self):
        self.off()
