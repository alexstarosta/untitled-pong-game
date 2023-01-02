##
##  Untitled Pong Game
##  August 2022 - January 2023
##  Alex Starosta
##

import pygame
import time
import settings
from elements import *
from menu import *

time.sleep(1)

programIcon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(programIcon)

pygame.mixer.init()

menu = Menu(settings.SFX, settings.PARTICLES, settings.GAMEMODE, "normal")
menu.setup()
menu.run()