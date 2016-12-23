# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Sending mouse position."""
import serial
import time


class DataSerial:

    """Serial communication."""
    limit = 50

    def __init__(self):
        """Initialize serial."""
        try:
            self.ser = serial.Serial('COM3', 9600, timeout=0)
            print "Connected to serial COM3"
        except:
            print "Could not connect to serial"

    def read_ser(self):
        """Read serial data."""
        while 1:
            print 'Read: ' + self.ser.readline()
            time.sleep(1)

    def send_ser(self, num):
        """Send number using serial."""
        y_string = self.string_number(num)
        print "Sent: " + y_string,
        self.ser.write(y_string)

    def close_ser(self):
        """Close serial."""
        self.ser.write("x")
        self.ser.flush()
        self.ser.close()

    def string_number(self, y):
        """Cast number to string."""
        y = 255.0 * y / DataSerial.limit
        return str(1000 + int(y))[-3:] + "\n"
