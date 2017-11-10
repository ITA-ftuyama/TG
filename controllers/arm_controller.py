#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Arm Controller."""
from serialcom.data_serial import DataSerial


class Controller:

    """Led Controller."""

    def __init__(self, view):
        """Creates new controller."""
        port = '/dev/ttyACM0'
        self.serial = DataSerial(view, port)

    def send_action(self, action):
        """Control Arm using serial."""
        if self.serial:
            c_action = {
                'idle': 'i',
                'blink': 'b',
                'punchleft': 'l',
                'punchright': 'r',
                'head': 'h'
            }.get(action, None)
            self.serial.send_ser(c_action)

    def control_arm(self, recorder):
        """Control Arm using serial."""
        try:
            attention  = int(recorder.attention[-1] / 2)
            meditation = int(recorder.meditation[-1] / 2)
            blink      = int(recorder.blink[-1] / 2)
            command    = [attention, meditation, blink]

            if self.serial:
                for number in command:
                    self.serial.send_ser(number)
        except:
            pass

    def close(self):
        """Close serial."""
        if self.serial:
            self.serial.close_ser()

