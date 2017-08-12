#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Pygame viewer."""
import pygame
from mindwave.pyeeg import bin_power
from mindwave.parser import ThinkGearParser, TimeSeriesRecorder
from mindwave.bluetooth_headset import BluetoothError
from startup import mindwave_startup
from controllers.controller import Controller
from random import randint
from numpy import *
from pygame import *
from view import View


def has_recorded(recorder):
    return len(recorder.attention) > 0 or len(recorder.meditation) > 0 or len(recorder.blink) > 0

def mock_data(parser):
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x80) + chr(3) + chr(0) + chr(randint(0,100)) + chr(0x00))
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x04) + chr(randint(0,100)) + chr(0x00))
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x05) + chr(randint(0,100)) + chr(0x00))
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x16) + chr(randint(0,100)) + chr(0x00))


def main():
    """Main loop capture."""
    view = View()
    controller = Controller('led')

    recorder = TimeSeriesRecorder()
    parser = ThinkGearParser(recorders=[recorder])

    socket, args = mindwave_startup(view=view, description="Pygame Example")
    fps_clock = pygame.time.Clock()

    mock = True
    raw_eeg = True
    spectra = []

    quit = False
    while quit is False:   
        try:
            if socket is not None:
                data = socket.recv(10000)
                parser.feed(data)
        except BluetoothError:
            view.flash_message("Bluetooth Error")
            pass
        if mock: mock_data(parser)
        view.gui()
        if has_recorded(recorder):
            flen = 50
            if len(recorder.raw) >= 500:
                spectrum, relative_spectrum = bin_power(
                    recorder.raw[-512 * 3:], range(flen), 512)
                spectra.append(array(relative_spectrum))
                if len(spectra) > 30:
                    spectra.pop(0)

                spectrum = mean(array(spectra), axis=0)
                view.print_spectrum(spectrum, flen)
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
            if raw_eeg:
                view.print_board()
                view.print_eeg(recorder)
        elif socket is None:
            view.print_message("disconnection")
            pass
        else:
            view.print_message("nothing")
            pass

        for event in pygame.event.get():
            quit = event.type == QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE
            )
        pygame.display.update()
        fps_clock.tick(12)

controller = None
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        if controller:
            controller.close()
