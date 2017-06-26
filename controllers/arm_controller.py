#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Arm Controller."""
from serialcom.data_serial import DataSerial


class Controller:

    """Led Controller."""

    def __init__(self):
        """Try openning new serial."""
        self.serial = DataSerial('/dev/ttyACM0')

    def control_arm(self, command):
        """Control Led using serial."""
        if self.serial:
            for number in command:
                self.serial.send_ser(number)

    def close(self):
        """Close serial."""
        if self.serial:
            self.serial.close_ser()

