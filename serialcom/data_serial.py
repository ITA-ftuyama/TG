# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Sending mouse position."""
import serial
import time


class DataSerial:

    """Serial communication."""
    limit = 50

    def __init__(self, view, port):
        """Initialize serial."""
        try:
            self.view = view
            self.ser = serial.Serial(port, 9600, timeout=0)
            self.view.print_message("Connected to serial " + port, "serial")
        except Exception as e:
            self.ser = None
            self.view.print_message("Could not connect to serial", "serial")

    def read_ser(self):
        """Read serial data."""
        while 1:
            self.view.add_message(self.ser.readline(), "rser_data")
            time.sleep(1)

    def send_ser(self, num):
        """Send number using serial."""
        y_string = self.string_number(num)
        self.view.add_message(y_string.rstrip(), "sser_data")
        self.ser.write(y_string)

    def close_ser(self):
        """Close serial."""
        if self.ser:
            self.ser.write("x")
            self.ser.flush()
            self.ser.close()

    def string_number(self, y):
        """Cast number to string."""
        y = 255.0 * y / DataSerial.limit
        return str(1000 + int(y))[-3:] + "\n"
