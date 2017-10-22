#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Pygame viewer."""
import time
from mindwave.pyeeg import bin_power
from mindwave.parser import ThinkGearParser, TimeSeriesRecorder
from mindwave.bluetooth_headset import BluetoothError
from startup import mindwave_startup
from controllers.controller import Controller
from random import randint
from numpy import *
from view import View

spectrum_mean = False

def has_recorded(recorder):
    return len(recorder.attention) > 0 or len(recorder.meditation) > 0 or len(recorder.blink) > 0

def mock_data(parser):
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x80) + chr(3) + chr(0) + chr(randint(0,100)) + chr(0x00))
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x04) + chr(randint(0,100)) + chr(0x00))
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x05) + chr(randint(0,100)) + chr(0x00))
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x16) + chr(randint(0,100)) + chr(0x00))

def main():
    """Main loop capture."""
    recorder = TimeSeriesRecorder()
    parser = ThinkGearParser(recorders=[recorder])

    view = View()
    controller = Controller(view, 'led')
    socket, args = mindwave_startup(view=view, description="TEEG")

    mock = True
    spectra = []

    while view.screen.quit is False:   
        try:
            if socket is not None:
                data = socket.recv(10000)
                parser.feed(data)
        except BluetoothError:
            view.print_message("Bluetooth Error", "status")
            pass
        if mock: 
            mock_data(parser)
        if has_recorded(recorder):
            flen = 50
            if len(recorder.raw) >= 500:
                spectrum, relative_spectrum = bin_power(
                    recorder.raw[-512 * 2:], range(flen), 512)

                # Mostrar a média spectral
                if spectrum_mean:
                    spectra.append(array(relative_spectrum))
                    if len(spectra) > 30:
                        spectra.pop(0)
                    spectrum = mean(array(spectra), axis=0)
                else:
                    spectrum = relative_spectrum

                view.update_spectrum(spectrum)
            else:
                pass

            view.print_waves(recorder)
            controller.control(recorder)

            """if len(parser.current_vector)>7:
                m = max(p.current_vector)
                for i in range(7):
                    if m == 0:
                        value = 0
                    else:
                        value = p.current_vector[i] *100.0/m
                    pygame.draw.rect(window, redColor,
                    (600+i*30,450-value, 6,value))"""
        elif socket is None:
            view.print_message("Mindwave not detected...", "status")
            pass
        else:
            view.print_message("Not receiving any data from mindwave...", "status")
            pass
        time.sleep(0.001)

controller = None
if __name__ == '__main__':
    try:
        main()
    finally:
        if controller:
            controller.close()
