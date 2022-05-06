from _Framework.ButtonElement import ButtonElement, Color
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.SysexValueControl import SysexValueControl
import logging
LAUNCHPAD_SYSEX_PREFIX = (240, 0, 32, 41, 2, 13)
LIGHT_SYSEX_PREFIX = LAUNCHPAD_SYSEX_PREFIX + (3,)

SOLID_TYPE    = 0
FLASHING_TYPE = 1
PULSING_TYPE  = 2

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
        self.send_value(self._getColorMidi(color), True)

    def flash(self, color = None):
        self._sysex.send_value((FLASHING_TYPE, self._address, self._getColorMidi(color), 0))  

    def pulse(self, color = None):
        self._sysex.send_value((PULSING_TYPE, self._address, self._getColorMidi(color)))   

    def off(self):
        self.send_value(0, True)

    def _getColorMidi(self, color = None):
        return color.midi_value if color != None else self._color.midi_value

    def reset(self):
        self.off()
