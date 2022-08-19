##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

import math
import pygame
import sys
from settings import *
from elements import *

gamestate = "inactive"

class Game:
    def __init__(self, gamestate):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.gamestate = gamestate
        self.gameCountdown = 3

    def setup(self):
        self.elements = pygame.sprite.Group()
        self.ballElements = pygame.sprite.Group()
        self.player1 = Player(self, WIDTH/50, HEIGHT/2 - HEIGHT/12, WIDTH/50, HEIGHT/6, 1)
        self.player2 = Player(self, WIDTH - 2*WIDTH/50, HEIGHT/2 - HEIGHT/12, WIDTH/50, HEIGHT/6, 2)
        self.ball = Ball(self, WIDTH/2, HEIGHT/2, 1*BALL_SPEED, 0.5*BALL_SPEED, WIDTH/50, WIDTH/50)

        gameFont = pygame.font.Font("bit5x5.ttf", 172)
        self.startingText = gameFont.render(f"{self.gameCountdown}", False, LIGHTGREY)
        self.startingTextRect = self.startingText.get_rect(center = (WIDTH/1.92, HEIGHT/4))

        self.draw()

    def draw(self):
        self.screen.fill(DARKGREY)
        self.elements.draw(self.screen)
        self.ballElements.draw(self.screen)
        self.screen.blit(self.startingText, self.startingTextRect)
        pygame.display.flip() 

    def drawCountdown(self, text):
        gameFont = pygame.font.Font("bit5x5.ttf", 172)
        self.startingText = gameFont.render(f"{text}", False, LIGHTGREY)
        self.startingTextRect = self.startingText.get_rect(center = (WIDTH/1.92, HEIGHT/4))
        self.screen.blit(self.startingText, self.startingTextRect)
        pygame.display.flip() 

    def run(self):
        self.playing = True
        self.gameState = "playing"
        while self.playing:
            self.tickspeed = self.clock.tick(FPS) / 1000.0
            self.elements.update()
            self.ballElements.update()
            self.draw()
            self.gameCountdown -= self.tickspeed
            
            if self.gameCountdown >= -0.1:
                if math.ceil(self.gameCountdown) == 3:
                    self.drawCountdown(3)
                elif math.ceil(self.gameCountdown) == 2:
                    self.drawCountdown(2) 
                elif math.ceil(self.gameCountdown) == 1:
                    self.drawCountdown(1)
                else:
                    self.drawCountdown("GO!")
                    self.ball.startGame()
                    self.gameState = "active"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
    
    def quit(self):
        pygame.quit()
        sys.exit()

game = Game(gamestate)
game.setup()
game.run()