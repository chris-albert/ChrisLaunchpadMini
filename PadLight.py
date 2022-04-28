from _Framework.SysexValueControl import SysexValueControl
from _Framework.InputControlElement import InputControlElement, MIDI_CC_TYPE

LAUNCHPAD_SYSEX_PREFIX = (240, 0, 32, 41, 2, 13)
LIGHT_SYSEX_PREFIX = LAUNCHPAD_SYSEX_PREFIX + (3,)

SOLID_TYPE    = 0
FLASHING_TYPE = 1
PULSING_TYPE  = 2

class PadLight:
    u"""
       address is the CC of the pad
       color is the default color to show if none specified
    """
    def __init__(self, address, color = None):
        self._address = address
        self._color = color
        self._sysex = SysexValueControl(LIGHT_SYSEX_PREFIX)
        self._input = InputControlElement(MIDI_CC_TYPE, 0, address)

    def solid(self, color = None):
        self._input.send_value(color.midi_value if color != None else self._color.midi_value)
        # self._sysex.send_value((SOLID_TYPE, self._address, color.midi_value))

    def flash(self, color = None):
        self._sysex.send_value((FLASHING_TYPE, self._address, color.midi_value, 0))    

    def pulse(self, color = None):
        self._sysex.send_value((PULSING_TYPE, self._address, color.midi_value)) 
    
    def off(self):
        self._input.send_value(0)

    def disconnect(self):
        self.off()   
