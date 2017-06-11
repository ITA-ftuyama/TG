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


description = """Pygame Example
"""

controller = Controller('led')
socket, args = mindwave_startup(description=description)
recorder = TimeSeriesRecorder()
parser = ThinkGearParser(recorders=[recorder])

blackColor  = pygame.Color(0, 0, 0)
whiteColor  = pygame.Color(255, 255, 255)
redColor    = pygame.Color(255, 0, 0)
greenColor  = pygame.Color(0, 255, 0)
deltaColor  = pygame.Color(100, 0, 0)
thetaColor  = pygame.Color(0, 0, 255)
alphaColor  = pygame.Color(255, 0, 0)
betaColor   = pygame.Color(0, 255, 00)
gammaColor  = pygame.Color(0, 255, 255)

mock = True


def wave_color(freq):
    """Color according to the wave."""
    if freq < 3:
        return deltaColor
    elif freq < 8:
        return thetaColor
    elif freq < 13:
        return alphaColor
    elif freq < 30:
        return betaColor
    else:
        return gammaColor


def print_attention(window, recorder):
    """Print attention level."""
    try:
        pygame.draw.circle(
            window, redColor, (800, 200), int(recorder.attention[-1] / 2))
        pygame.draw.circle(window, greenColor, (800, 200), 60 / 2, 1)
        pygame.draw.circle(window, greenColor, (800, 200), 100 / 2, 1)
        window.blit(attention_img, (760, 260))
    except:
        return


def print_meditation(window, recorder):
    """Print meditation level."""
    try:
        pygame.draw.circle(
            window, redColor, (650, 200), int(recorder.meditation[-1] / 2))
        pygame.draw.circle(window, greenColor, (650, 200), 60 / 2, 1)
        pygame.draw.circle(window, greenColor, (650, 200), 100 / 2, 1)

        window.blit(meditation_img, (600, 260))
    except:
        return

def print_blink(window, recorder):
    """Print blink level."""
    try:
        pygame.draw.circle(
            window, redColor, (500, 200), int(recorder.blink[-1] / 2))
        pygame.draw.circle(window, greenColor, (500, 200), 60 / 2, 1)
        pygame.draw.circle(window, greenColor, (500, 200), 100 / 2, 1)

        window.blit(blink_img, (460, 260))
    except:
        return


def print_spectrum(window, spectrum, flen):
    """Print mind wave spectrum."""
    for i in range(flen - 1):
        value = float(spectrum[i] * 1000)
        color = wave_color(i)
        pygame.draw.rect(
            window, color, (25 + i * 10, 400 - value, 5, value))


def print_eeg(window, recorder):
    """Print EEG record."""
    lv = 0
    for i, value in enumerate(recorder.raw[-1000:]):
        v = value / 2.0
        pygame.draw.line(
            window, redColor, (i + 25, 500 - lv), (i + 25, 500 - v))
        lv = v


def print_nothing(window, font):
    """Print data not detected."""
    img = font.render(
        "Not receiving any data from mindwave...", False, redColor)
    window.blit(img, (100, 100))


def print_disconnection(window, font):
    """Device not detected."""
    img = font.render(
        "Mindwave not detected...", False, whiteColor)
    window.blit(img, (100, 100))

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

    pygame.init()

    fps_clock = pygame.time.Clock()

    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Mindwave Viewer")

    background_img = pygame.image.load("assets/pygame_background.png")

    font = pygame.font.Font("freesansbold.ttf", 20)
    raw_eeg = True
    spectra = []

    meditation_img = font.render("Meditation", False, redColor)
    attention_img = font.render("Attention", False, redColor)
    blink_img = font.render("Blink", False, redColor)

    quit = False
    while quit is False:   
        try:
            if socket is not None:
                data = socket.recv(10000)
                parser.feed(data)
        except BluetoothError:
            pass
        if mock: mock_data()
        window.blit(background_img, (0, 0))
        if has_recorded():
            flen = 50
            if len(recorder.raw) >= 500:
                spectrum, relative_spectrum = bin_power(
                    recorder.raw[-512 * 3:], range(flen), 512)
                spectra.append(array(relative_spectrum))
                if len(spectra) > 30:
                    spectra.pop(0)

                spectrum = mean(array(spectra), axis=0)
                print_spectrum(window, spectrum, flen)
            else:
                pass
            print_attention(window, recorder)
            print_meditation(window, recorder)
            print_blink(window, recorder)

            # controller.control(recorder)

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
                print_eeg(window, recorder)
        elif socket is None:
            print_disconnection(window, font)
            pass
        else:
            print_nothing(window, font)
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
