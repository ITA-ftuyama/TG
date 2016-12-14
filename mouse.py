# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Win32api demo."""
import win32api
import win32con


def position():
	"""Get x position."""
    a, b = win32api.GetCursorPos()
    print a


def click(x, y):
	"""Click with mouse."""
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
position()
click(10, 10)
