#!/usr/bin/python
# -*- coding: utf-8 -*-
"""ViewController."""
import pygame
import struct

pygame.init()

# General Colors
blackColor  = pygame.Color("#000000")
whiteColor  = pygame.Color("#FFFFFF")
redColor    = pygame.Color("#FF0000")
greenColor  = pygame.Color("#00FF00")
blueColor   = pygame.Color("#0000FF")
deltaColor  = pygame.Color("#AA0000")
thetaColor  = pygame.Color("#00AA00")
alphaColor  = pygame.Color("#0000AA")
betaColor   = pygame.Color("#AAAA00")
gammaColor  = pygame.Color("#00AAAA")

# GUI pallete
backColor    = pygame.Color("#466666")
titleColor   = pygame.Color("#330000")

# Fonts
font_20 = pygame.font.Font("freesansbold.ttf", 20)
font_28 = pygame.font.Font("freesansbold.ttf", 28)


class View(object):

    def __init__(self):
        self.window = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Mindwave Viewer")

        meditation_img = font_20.render("Meditation", False, redColor)
        attention_img  = font_20.render("Attention", False, redColor)
        blink_img      = font_20.render("Blink", False, redColor)


    def gui(self):
        self.window.fill(backColor)
        self.window.blit(
            font_28.render("Mindwave Controller", False, titleColor), 
            (50, 50))
        pygame.display.update()


    def print_message(self, message):
        """Device not detected."""
        self.gui()
        self.window.blit(
            font_20.render(message, False, whiteColor), 
            (50, 100))
        pygame.display.update()


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

    def print_board(window):
        """Print EEG board."""
        pygame.draw.line(window, blueColor, (25,   500), (1025, 500))
        pygame.draw.line(window, blueColor, (25,   400), (1025, 400))
        pygame.draw.line(window, blueColor, (25,   600), (1025, 600))
        pygame.draw.line(window, blueColor, (25,   400), (25,   600))
        pygame.draw.line(window, blueColor, (1025, 400), (1025, 600))


    def print_eeg(window, recorder):
        """Print EEG record."""
        lv = 0
        for i, value in enumerate(recorder.raw[-1000:]):
            v = value / 5.0
            pygame.draw.line(
                window, redColor, (i + 25, 500 - lv), (i + 25, 500 - v))
            lv = v


    def print_waves(window, font):
        """Print word on screen."""
        window.blit(font.render("Delta", False, deltaColor), (25,  400))
        window.blit(font.render("Theta", False, thetaColor), (50,  425))
        window.blit(font.render("Alpha", False, alphaColor), (100, 400))
        window.blit(font.render("Beta",  False, betaColor),  (150, 425))
        window.blit(font.render("Gamma", False, gammaColor), (350, 400))


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
