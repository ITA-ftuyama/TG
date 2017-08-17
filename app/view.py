#!/usr/bin/python
# -*- coding: utf-8 -*-
"""ViewController."""
import pygame
import struct
from pgu import gui
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg

app = gui.App()
e = gui.Button("Hello World")

c = gui.Container(align=-1,valign=-1)
c.add(e,0,0)

app.init(c)

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
titleColor   = pygame.Color("#660000")

# Fonts
font_14 = pygame.font.Font("freesansbold.ttf", 14)
font_20 = pygame.font.Font("freesansbold.ttf", 20)
font_32 = pygame.font.Font("freesansbold.ttf", 32)

# Words
meditation_img = font_20.render("Meditation", False, redColor)
attention_img  = font_20.render("Attention", False, redColor)
blink_img      = font_20.render("Blink", False, redColor)


class View(object):

    def __init__(self):
        self.window = pygame.display.set_mode((1200, 700))
        self.bd = [[25, 1025], [400, 600, 500]]
        pygame.display.set_caption("Mindwave Viewer")
        self.messages = {
            "bluetooth": [],
            "serial": [],
            "status": [],
            "sser_data": []
        }
        self.gui()

    def graph(self, recorder):
        """Print some graph."""
        fig = pylab.figure(figsize=[4, 4], # Inches
                           dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        ax.plot(recorder.raw[-1000:])

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        screen = pygame.display.get_surface()
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (400,300))

    def gui(self):
        """Print some GUI."""
        self.window.fill(backColor)
        self.window.blit(font_32.render("Mindwave Controller", False, titleColor), (50, 50))
        app.paint()

    def substr(self, messages):
        """Print cropped message."""
        msg = ", ".join(messages)
        return msg[-100:]

    def print_message(self, message, kind):
        """Print some messages."""
        if message is not None:
            self.messages[kind].append(message)

        self.window.blit(font_20.render(self.substr(self.messages["bluetooth"]),  False, blueColor),  (50, 100))
        self.window.blit(font_20.render(self.substr(self.messages["serial"]),     False, redColor),   (50, 125))
        self.window.blit(font_20.render(self.substr(self.messages["status"]),     False, whiteColor), (50, 150))
        self.window.blit(font_14.render("Sent Serial: " + "; ".join(self.messages["sser_data"]),   False, redColor),   (50, 175))

    def add_message(self, message, kind):
        """Add some messages."""
        self.messages[kind].append(message)
        if len(self.messages[kind]) > 10:
            self.messages[kind].pop(0)

    def flash_message(self, message, kind):
        self.gui()
        self.print_message(message, kind)
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
            pygame.draw.circle(self.window, redColor, position, value)
            pygame.draw.circle(self.window, greenColor, position, 30, 1)
            pygame.draw.circle(self.window, greenColor, position, 50, 1)
        except:
            return

    def print_waves(self, recorder):
        """Print word on screen."""
        pos_y = 350
        self.print_message(None, None)
        self.window.blit(font_20.render("Delta", False, deltaColor), (25,  pos_y))
        self.window.blit(font_20.render("Theta", False, thetaColor), (50,  pos_y + 25))
        self.window.blit(font_20.render("Alpha", False, alphaColor), (100, pos_y))
        self.window.blit(font_20.render("Beta",  False, betaColor),  (150, pos_y + 25))
        self.window.blit(font_20.render("Gamma", False, gammaColor), (350, pos_y))

        pos_x = 650
        pos_y = 200

        self.graph(recorder)

        """Print blink level."""
        position = (pos_x, pos_y)
        self.print_circle(position, int(recorder.blink[-1] / 2))
        self.window.blit(blink_img, (pos_x - 20, pos_y + 60))

        """Print meditation level."""
        position = (pos_x + 150, pos_y)
        self.print_circle(position, int(recorder.meditation[-1] / 2))
        self.window.blit(meditation_img, (pos_x + 100, pos_y + 60))

        """Print attention level."""
        position = (pos_x + 300, pos_y)
        self.print_circle(position, int(recorder.attention[-1] / 2))
        self.window.blit(attention_img, (pos_x + 260, pos_y + 60))

