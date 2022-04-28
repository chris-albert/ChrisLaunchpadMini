from _Framework.ButtonElement import ButtonElement, Color
from _Framework.InputControlElement import MIDI_CC_TYPE
import logging

class MyButton(ButtonElement):

    def __init__(self, address, color = None, on_click = None, start_on = True):
      super(MyButton, self).__init__(False, MIDI_CC_TYPE, 0, address)
      self._color = color
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

    def off(self):
        self.send_value(0, True)

    def _getColorMidi(self, color = None):
        return color.midi_value if color != None else self._color.midi_value

    def reset(self):
        self.send_value(0, True)
