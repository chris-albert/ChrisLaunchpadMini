#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Mini_MK3/__init__.py
# from __future__ import absolute_import, print_function, unicode_literals
from .launchpad_mini_mk3 import Launchpad_Mini_MK3

def create_instance(c_instance):
    return Launchpad_Mini_MK3(c_instance=c_instance)
