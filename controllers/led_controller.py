#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Led Controller."""
from serialcom.data_serial import DataSerial


class Controller:

    """Led Controller."""

    def __init__(self, view, port):
        """Try openning new serial."""
        self.serial = DataSerial(view, port)

    def control_led(self, number):
        """Control Led using serial."""
        if self.serial:
            self.serial.send_ser(number)

    def close(self):
        """Close serial."""
        if self.serial:
            self.serial.close_ser()
