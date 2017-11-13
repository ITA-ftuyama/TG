#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Arm Controller."""
from serialcom.data_serial import DataSerial


class Controller:

    """Led Controller."""

    def __init__(self, view):
        """Creates new controller."""
        self.serial = DataSerial(view)

    def send_action(self, action):
        """Control Arm using serial."""
        if self.serial and self.serial.ser:
            c_action = {
                'idle': 'i',
                'blink': 'b',
                'punchleft': 'l',
                'punchright': 'r',
                'head': 'h',
                'tooth': 't',
                'closedeyes': 'c',
                'closedeyeshand': 'm'
            }.get(action, None)
            self.serial.send_action(c_action)

    def control_arm(self, recorder):
        """Control Arm using serial."""
        try:
            attention  = int(recorder.attention[-1] / 2)
            meditation = int(recorder.meditation[-1] / 2)
            blink      = int(recorder.blink[-1] / 2)
            command    = [attention, meditation, blink]

            if self.serial and self.serial.ser:
                for number in command:
                    self.serial.send_ser(number)
        except:
            pass

    def close(self):
        """Close serial."""
        if self.serial and self.serial.ser:
            self.serial.close_ser()

