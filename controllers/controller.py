#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Controller."""
from led_controller import Controller as LedController
from arm_controller import Controller as ArmController

class Controller:

    """Controller Facade."""

    def __init__(self, kind):
        """Creates new controller."""
        port = '/dev/ttyACM1'
        self.kind = kind
        if kind == 'led':
            self.controller = LedController(port)
        if kind == 'arm':
            self.controller = ArmController(port)

    def control(self, recorder):
        """Control using recorder."""
        try:
            attention  = int(recorder.attention[-1] / 2)
            meditation = int(recorder.meditation[-1] / 2)
            blink      = int(recorder.blink[-1] / 2)

            if self.kind == 'led':
                self.controller.control_led(attention)
            if self.kind == 'arm':
                self.controller.control_led([attention, meditation, blink])
        except:
            pass


    def close(self):
        """Close controller."""
        self.controller.close()
