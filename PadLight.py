from _Framework.SysexValueControl import SysexValueControl

LAUNCHPAD_SYSEX_PREFIX = (240, 0, 32, 41, 2, 13)
LIGHT_SYSEX_PREFIX = LAUNCHPAD_SYSEX_PREFIX + (3,)

SOLID_TYPE    = 0
FLASHING_TYPE = 1
PULSING_TYPE  = 2

class PadLight:
    u"""
       address is the CC of the pad
    """
    def __init__(self, address):
        self._address = address
        self._sysex = SysexValueControl(LIGHT_SYSEX_PREFIX)

    def solid(self, color):
        self._sysex.send_value((SOLID_TYPE, self._address, color.midi_value))

    def flash(self, color):
        self._sysex.send_value((FLASHING_TYPE, self._address, color.midi_value, 0))    

    def pulse(self, color):
        self._sysex.send_value((PULSING_TYPE, self._address, color.midi_value)) 
    
    def off(self):
        self._sysex.send_value((SOLID_TYPE, self._address, 0))      

    def disconnect(self):
        self.off()   
