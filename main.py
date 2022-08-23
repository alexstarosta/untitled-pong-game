##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

from settings import *
from elements import *
from game import *

gamestate = "inactive"
game = Game(gamestate)
game.setup()
game.run()