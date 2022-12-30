##
##  Untitled Pong Game
##  August 2022 - January 2023
##  Alex Starosta
##

from settings import *
from elements import *
from menu import *

menu = Menu(SFX, PARTICLES, GAMEMODE, "normal")
menu.setup()
menu.run()