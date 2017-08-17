"""<title>Integration with a Game</title>
For games, it is usually preferrable to not have your game within
a GUI framework.  This GUI framework can be placed within your game.
"""

import time
import random
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

# The maximum frame-rate
FPS = 30
WIDTH,HEIGHT = 640,480

##You can initialize the screen yourself.
##::
screen = pygame.display.set_mode((640,480),SWSURFACE)
##


form = gui.Form()

app = gui.App()
e = gui.Button("Hello World")

c = gui.Container(align=-1,valign=-1)
c.add(e,0,0)

app.init(c)
##

dist = 8192
span = 10
stars = []

##You can include your own run loop.
##::
clock = pygame.time.Clock()
done = False
font_20 = pygame.font.Font("freesansbold.ttf", 20)
while not done:
    for e in pygame.event.get():
        if e.type is QUIT: 
            done = True
        elif e.type is KEYDOWN and e.key == K_ESCAPE: 
            done = True
        else:
            app.event(e)

    # Clear the screen and render the stars
    dt = clock.tick(FPS)/1000.0
    screen.fill((0,0,0))
    screen.blit(font_20.render("as", False, pygame.Color("#00AAAA")), (50, 100))
    app.paint()
    pygame.display.flip()
