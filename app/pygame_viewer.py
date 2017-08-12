#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Pygame viewer."""
import pygame
from mindwave.pyeeg import bin_power
from mindwave.parser import ThinkGearParser, TimeSeriesRecorder
from mindwave.bluetooth_headset import BluetoothError
from example_startup import mindwave_startup
from controllers.controller import Controller
from random import randint
from numpy import *
from pygame import *
from view import View


description = """Pygame Example
"""

controller = Controller('led')
recorder = TimeSeriesRecorder()
parser = ThinkGearParser(recorders=[recorder])

mock = False

def has_recorded():
    return len(recorder.attention) > 0 or len(recorder.meditation) > 0 or len(recorder.blink) > 0

def mock_data():
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x80) + chr(3) + chr(0) + chr(randint(0,100)) + chr(0x00))
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x04) + chr(randint(0,100)) + chr(0x00))
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x05) + chr(randint(0,100)) + chr(0x00))
    parser.feed(chr(0xaa) + chr(0xaa) + chr(3) + chr(0x16) + chr(randint(0,100)) + chr(0x00))


def main():
    """Main loop capture."""
    global meditation_img, attention_img, blink_img

    view = View()
    socket, args = mindwave_startup(view=view, description=description)
    fps_clock = pygame.time.Clock()

    raw_eeg = True
    spectra = []

    quit = False
    while quit is False:   
        try:
            if socket is not None:
                data = socket.recv(10000)
                parser.feed(data)
        except BluetoothError:
            pass
        if mock: mock_data()
        view.gui()
        if has_recorded():
            flen = 50
            if len(recorder.raw) >= 500:
                spectrum, relative_spectrum = bin_power(
                    recorder.raw[-512 * 3:], range(flen), 512)
                spectra.append(array(relative_spectrum))
                if len(spectra) > 30:
                    spectra.pop(0)

                spectrum = mean(array(spectra), axis=0)
                #print_spectrum(window, spectrum, flen)
            else:
                pass
            #print_attention(window, recorder)
            #print_meditation(window, recorder)
            #print_blink(window, recorder)
            #print_waves(window, font)

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
                print_board(window)
                print_eeg(window, recorder)
        elif socket is None:
            #print_disconnection(window, font)
            pass
        else:
            #print_nothing(window, font)
            pass

        for event in pygame.event.get():
            quit = event.type == QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE
            )
        pygame.display.update()
        fps_clock.tick(12)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        controller.close()
