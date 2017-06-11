#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Controller."""
from led_controller import Controller as LedController
from arm_controller import Controller as ArmController

class Controller:

    """Controller Facade."""

    def __init__(self, kind):
        """Creates new controller."""
        if kind == 'led':
            self.controller = LedController()
        if kind == 'arm':
            self.controller = ArmController()

    def control(self, recorder):
        """Control using recorder."""
        attention  = int(recorder.attention[-1] / 2)
        meditation = int(recorder.meditation[-1] / 2)
        blink      = int(recorder.blink[-1] / 2)

        if control == 'led':
            self.controller.control_led(attention)
        if control == 'arm':
            self.controller.control_led([attention, meditation, blink])

    def close(self):
        """Close controller."""
        self.controller.close()
