#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Led Controller."""
from serialcom.data_serial import DataSerial


class Controller:

    """Led Controller."""

    def __init__(self, view):
        """Try openning new serial."""
        port = '/dev/ttyACM0'
        self.serial = DataSerial(view, port)

    def control_led(self, number):
        """Control Led using serial."""
        try:
            attention  = int(recorder.attention[-1] / 2)
            meditation = int(recorder.meditation[-1] / 2)
            blink      = int(recorder.blink[-1] / 2)

            if self.serial:
                self.serial.send_ser(attention)
        except:
            pass

    def close(self):
        """Close serial."""
        if self.serial:
            self.serial.close_ser()
