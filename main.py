##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

from settings import *
from elements import *
from game import *
from menu import *

def startGame():
    gamestate = "inactive"
    game = Game(gamestate)
    game.setup()
    game.run()

menu = Menu()
menu.setup()
menu.run()