##
##  Untitled Pong Game
##  August 2022 - January 2023
##  Alex Starosta
##

import pygame
from settings import *
from elements import *
from menu import *

programIcon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(programIcon)

pygame.mixer.init()

menu = Menu(SFX, PARTICLES, GAMEMODE, "normal")
menu.setup()
menu.run()