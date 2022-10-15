##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

import math
from re import S
import pygame
import sys
from settings import *
from elements import *

class Game:
    def __init__(self, gamestate, gamemode, sfx, particle):
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.gameMode = gamemode
        self.sfx = sfx
        self.particles = particle
        self.gamestate = gamestate
        self.keycheck = True
        self.gameCountdown = 3
        self.score = [0,0]

    def setup(self):

        self.elements = pygame.sprite.Group()
        self.ballElements = pygame.sprite.Group()

        if self.particles == "on":
            self.particleSpawner = ParticleSpawner()

        self.player1 = Player(self, WIDTH/50, HEIGHT/2 - HEIGHT/12, WIDTH/50, HEIGHT/6, 1)
        self.player2 = Player(self, WIDTH - 2*WIDTH/50 + 1, HEIGHT/2 - HEIGHT/12, WIDTH/50, HEIGHT/6, 2)
        self.ball = Ball(self, WIDTH/2 - ((WIDTH/50)/2), HEIGHT/2, 1*BALL_SPEED, 0.0*BALL_SPEED, WIDTH/50, WIDTH/50)

        self.wsd1nonscaled = pygame.image.load("wsd1.png")
        self.wsd1 = pygame.transform.scale(self.wsd1nonscaled, (220,220))
        self.wsd1Rect = self.wsd1.get_rect(center = (WIDTH/2 - 200,HEIGHT/4))

        self.wkeyCheck = KeybindChecker(self, "w", WIDTH/4 - 50, HEIGHT/3 - 170, 100, 100, DARKBLUE)
        self.skeyCheck = KeybindChecker(self, "s", WIDTH/4 - 50, HEIGHT/3 - 60, 100, 100, DARKBLUE)
        self.dkeyCheck = KeybindChecker(self, "d", WIDTH/4 + 60, HEIGHT/3 - 120, 100, 100, DARKBLUE)

        self.upkeyCheck = KeybindChecker(self, "up", WIDTH/2 + WIDTH/4 - 50, HEIGHT/3 - 170, 100, 100, DARKRED)
        self.downkeyCheck = KeybindChecker(self, "down", WIDTH/2 + WIDTH/4 - 50, HEIGHT/3 - 60, 100, 100, DARKRED)
        self.leftkeyCheck = KeybindChecker(self, "left", WIDTH/2 + WIDTH/4 - 160, HEIGHT/3 - 120, 100, 100, DARKRED)

        self.udl1nonscaled = pygame.image.load("updownleft1.png")
        self.udl1 = pygame.transform.scale(self.udl1nonscaled, (220,220))
        self.udl1Rect = self.udl1.get_rect(center = (WIDTH/2 + 200,HEIGHT/4))

        gameFont5x5 = pygame.font.Font("bit5x5.ttf", 172)
        self.startingText = gameFont5x5.render("", False, LIGHTGREY)
        self.startingTextRect = self.startingText.get_rect(center = (WIDTH/1.92 - ((WIDTH/50)/2), HEIGHT/4))

        gameFont5x3 = pygame.font.Font("bit5x3.ttf", 112)
        if self.score[0] < 10:
            self.score1 = gameFont5x3.render("0" + f"{self.score[0]}", False, LIGHTGREY)
        else:
            self.score1 = gameFont5x3.render(f"{self.score[0]}", False, LIGHTGREY)
        self.score1Rect = self.score1.get_rect(center = (77.5, 65))

        if self.score[1] < 10:
            self.score2 = gameFont5x3.render("0" + f"{self.score[1]}", False, LIGHTGREY)
        else:
            self.score2 = gameFont5x3.render(f"{self.score[1]}", False, LIGHTGREY)
        self.score2Rect = self.score2.get_rect(center = (WIDTH-62.5, 65))

        self.draw()

    def draw(self):

        def changeColor(image, color):
            colouredImage = pygame.Surface(image.get_size())
            colouredImage.fill(color)
        
            finalImage = image.copy()
            finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
            return finalImage

        self.screen.fill(DARKGREY)
        self.elements.draw(self.screen)
        self.ballElements.draw(self.screen)
        self.screen.blit(self.startingText, self.startingTextRect)
        self.screen.blit(self.score1, self.score1Rect)
        self.screen.blit(self.score2, self.score2Rect)

        self.screen.blit(changeColor(self.wsd1, LIGHTGREY), self.wsd1Rect)
        self.screen.blit(changeColor(self.udl1, LIGHTGREY), self.udl1Rect)

        if self.particles == "on":
            self.particleSpawner.particleGroup.draw(self.screen)
        pygame.display.flip()

    def drawCountdown(self, text):
        gameFont = pygame.font.Font("bit5x5.ttf", 172)
        self.startingText = gameFont.render(f"{text}", False, LIGHTGREY)
        self.startingTextRect = self.startingText.get_rect(center = (WIDTH/1.92 - ((WIDTH/50)/2), HEIGHT/4))

        self.screen.blit(self.startingText, self.startingTextRect)
        pygame.display.flip() 

    def drawScores(self):
        gameFont5x3 = pygame.font.Font("bit5x3.ttf", 112)
        if self.score[0] < 10:
            self.score1 = gameFont5x3.render("0" + f"{self.score[0]}", False, LIGHTGREY)
        else:
            self.score1 = gameFont5x3.render(f"{self.score[0]}", False, LIGHTGREY)
        self.score1Rect = self.score1.get_rect(center = (77.5, 65))

        if self.score[1] < 10:
            self.score2 = gameFont5x3.render("0" + f"{self.score[1]}", False, LIGHTGREY)
        else:
            self.score2 = gameFont5x3.render(f"{self.score[1]}", False, LIGHTGREY)
        self.score2Rect = self.score2.get_rect(center = (WIDTH-62.5, 65))

        self.screen.blit(self.score1, self.score1Rect)
        self.screen.blit(self.score2, self.score2Rect)
        pygame.display.flip() 

    def run(self):
        self.playing = True
        self.gameState = "playing"
        while self.playing:
            self.tickspeed = self.clock.tick(FPS) / 1000.0
            self.elements.update()
            self.ballElements.update()
            self.draw()

            if self.particles == "on":
                self.particleSpawner.update()

            if self.keycheck:
                self.gameCountdown -= self.tickspeed
    
                if self.gameCountdown >= -3:
                    if math.ceil(self.gameCountdown) == 3:
                        self.drawCountdown(3)
                    elif math.ceil(self.gameCountdown) == 2:
                        self.drawCountdown(2) 
                    elif math.ceil(self.gameCountdown) == 1:
                        self.drawCountdown(1)
                    elif math.ceil(self.gameCountdown) == 0 and self.gameState == "playing":
                        self.drawCountdown("GO!")
                        self.ball.startGame()
                        self.gameState = "active"
                    elif math.ceil(self.gameCountdown) == -1:
                        self.drawCountdown("")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
    
    def quit(self):
        pygame.quit()
        sys.exit()