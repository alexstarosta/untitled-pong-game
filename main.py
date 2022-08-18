##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

import random
import pygame
import sys
from settings import *
from elements import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def setup(self):
        self.elements = pygame.sprite.Group()
        self.ballElements = pygame.sprite.Group()
        self.player1 = Player(self, WIDTH/50, HEIGHT/2 - HEIGHT/12, WIDTH/50, HEIGHT/6, 1)
        self.player2 = Player(self, WIDTH - 2*WIDTH/50, HEIGHT/2 - HEIGHT/12, WIDTH/50, HEIGHT/6, 2)
        self.ball = Ball(self, WIDTH/2, HEIGHT/2, 1*BALL_SPEED, -0.75*BALL_SPEED, WIDTH/50, WIDTH/50)
        self.draw()

    def draw(self):
        self.screen.fill(DARKGREY)
        self.elements.draw(self.screen)
        self.ballElements.draw(self.screen)
        pygame.display.flip()

    def run(self):
        self.playing = True
        while self.playing:
            self.tickspeed = self.clock.tick(FPS) / 1000.0
            self.elements.update()
            self.ballElements.update()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
    
    def quit(self):
        pygame.quit()
        sys.exit()

game = Game()
game.setup()
game.run()