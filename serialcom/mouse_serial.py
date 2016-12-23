# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Sending mouse position."""
import serial
import time
import win32api
ser = serial.Serial('COM3', 9600, timeout=0)
height = win32api.GetSystemMetrics(1)


def read_ser():
    """Read serial data."""
    while 1:
        print 'reading'
        print ser.readline()
        time.sleep(1)


def send_pos(n):
    """Send mouse position using serial."""
    for i in range(n):
        x, y = win32api.GetCursorPos()
        y_string = string_number(y)
        print y_string,
        ser.write(y_string)
        time.sleep(0.1)
    ser.write("x")
    ser.flush()
    ser.close()


def string_number(y):
    """Cast number to string."""
    y = (height - y) * 255 / height
    return str(1000 + int(y))[-3:] + "\n"

send_pos(1000)
