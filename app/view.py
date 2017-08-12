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

# Words
meditation_img = font_20.render("Meditation", False, redColor)
attention_img  = font_20.render("Attention", False, redColor)
blink_img      = font_20.render("Blink", False, redColor)


class View(object):

    def __init__(self):
        self.window = pygame.display.set_mode((1200, 800))
        self.bd = [[25, 1025], [400, 600, 500]]
        pygame.display.set_caption("Mindwave Viewer")

    def gui(self):
        self.window.fill(backColor)
        self.window.blit(
            font_28.render("Mindwave Controller", False, titleColor), 
            (50, 50))

    def print_message(self, message):
        """Print some message."""
        font = font_20
        color = whiteColor
        position = (100, 100)

        if message == "disconnection":
            message = "Mindwave not detected..."
        elif message == "nothing":
            message = "Not receiving any data from mindwave..."
            color = redColor
        else:
            position = (50, 100)

        self.window.blit(font.render(message, False, color), position)

    def flash_message(self, message):
        self.gui()
        self.print_message(message)
        pygame.display.update()


    def wave_color(self, freq):
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

    def print_spectrum(self, spectrum, flen):
        """Print mind wave spectrum."""
        for i in range(flen - 1):
            value = float(spectrum[i] * 1000)
            color = self.wave_color(i)
            pygame.draw.rect(
                self.window, color, (25 + i * 10, 400 - value, 5, value))

    def print_board(self):
        """Print EEG board."""
        bd = self.bd
        pygame.draw.line(self.window, blueColor, (bd[0][0], bd[1][2]), (bd[0][1], bd[1][2]))
        pygame.draw.line(self.window, blueColor, (bd[0][0], bd[1][0]), (bd[0][1], bd[1][0]))
        pygame.draw.line(self.window, blueColor, (bd[0][0], bd[1][1]), (bd[0][1], bd[1][1]))
        pygame.draw.line(self.window, blueColor, (bd[0][0], bd[1][0]), (bd[0][0], bd[1][1]))
        pygame.draw.line(self.window, blueColor, (bd[0][1], bd[1][0]), (bd[0][1], bd[1][1]))


    def print_eeg(self, recorder):
        """Print EEG record."""
        lv = 0
        bd = self.bd
        for i, value in enumerate(recorder.raw[-1000:]):
            v = value / 5.0
            pygame.draw.line(
                self.window, redColor, (i + bd[0][0], bd[1][2] - lv), (i + bd[0][0], bd[1][2] - v))
            lv = v


    def print_circle(self, position, value):
        """Print circle on screen."""
        try:
            pygame.draw.circle(
                self.window, redColor, position, value)
            pygame.draw.circle(self.window, greenColor, position, 60 / 2, 1)
            pygame.draw.circle(self.window, greenColor, position, 100 / 2, 1)
        except:
            return

    def print_waves(self, recorder):
        """Print word on screen."""
        pos_y = 350
        self.window.blit(font_20.render("Delta", False, deltaColor), (25,  pos_y))
        self.window.blit(font_20.render("Theta", False, thetaColor), (50,  pos_y + 25))
        self.window.blit(font_20.render("Alpha", False, alphaColor), (100, pos_y))
        self.window.blit(font_20.render("Beta",  False, betaColor),  (150, pos_y + 25))
        self.window.blit(font_20.render("Gamma", False, gammaColor), (350, pos_y))

        """Print attention level."""
        position = (800, 200)
        self.print_circle(position, int(recorder.attention[-1] / 2))
        self.window.blit(attention_img, (760, 260))

        """Print meditation level."""
        position = (650, 200)
        self.print_circle(position, int(recorder.meditation[-1] / 2))
        self.window.blit(meditation_img, (600, 260))

        """Print blink level."""
        position = (500, 200)
        self.print_circle(position, int(recorder.blink[-1] / 2))
        self.window.blit(blink_img, (460, 260))

