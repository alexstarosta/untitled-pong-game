##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

import pygame
import math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, pwidth, pheight, player):
        self.groups = game.elements
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([pwidth, pheight])
        if player == 1:
            self.image.fill(BLUE)
        elif player == 2:
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.velocity = 0
        self.direction = "none"
        self.height = pheight
        self.player = player
        self.rect.x = x
        self.rect.y = y
        self.y = y

    def getInput(self):
        if self.player == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.velocity = -PADDLE_SPEED
                self.direction = "up"
            if keys[pygame.K_s]:
                self.velocity = PADDLE_SPEED
                self.direction = "down"
            if self.velocity != 0: 
                self.velocity *= 0.7

        if self.player == 2:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.velocity = -PADDLE_SPEED
                self.direction = "up"
            if keys[pygame.K_DOWN]:
                self.velocity = PADDLE_SPEED
                self.direction = "down"
            if self.velocity != 0: 
                self.velocity *= 0.7

    def checkPlacement(self, direction):
        if direction == "up":
            if self.rect.top < 0:
                self.velocity = 0
                self.direction = "none"

        if direction == "down":
            if self.rect.bottom > HEIGHT:
                self.velocity = 0 
                self.direction = "none"

    def update(self):
        self.getInput()
        self.checkPlacement(self.direction)
        self.y += self.velocity
        self.rect.y = self.y

class Ball(pygame.sprite.Sprite):
    def __init__(self, game, x, y, xVel, yVel, bwidth, bheight):
        self.groups = game.ballElements
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([bwidth, bheight])
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = bwidth
        self.height = bheight
        self.prexVel = xVel
        self.preyVel = yVel
        self.xVel = 0
        self.yVel = 0
        self.rect.x = x
        self.rect.y = y
        self.originy = y - self.height/2
        self.originx = x
        self.y = y - self.height/2
        self.x = x
        self.bounceCount = 0
        self.side = "unknown"

    def startGame(self):
        self.bounceCount = 0
        self.y = self.originy
        self.x = self.originx
        self.startBall(self.prexVel,self.preyVel)

    def startBall(self, xVel, yVel):
        self.xVel = xVel
        self.yVel = yVel

    def increaseSpeed(self, amount):
        if self.xVel > 0.01:
            self.xVel += amount
        else:
            self.xVel -= amount

    def checkWalls(self):
        if self.y < 0 or self.y > HEIGHT - self.height:
            self.yVel *= -1
        if self.x < 0 or self.x > WIDTH - self.width:
            self.xVel *= -1
        if self.x < WIDTH/2 and pygame.sprite.spritecollideany(self, self.game.elements):
            self.xVel = abs(self.xVel)
            if self.side == "unknown" or self.side == "left":
                self.calcYVel(self.game.elements.sprites()[0], self.game.elements.sprites()[1], self.y, self.x, "left")
                self.side = "right"
                #self.increaseSpeed(0.2)
                self.bounceCount += 1
        if self.x > WIDTH/2 and pygame.sprite.spritecollideany(self, self.game.elements):
            self.xVel = -abs(self.xVel)
            if self.side == "unknown" or self.side == "right":
                self.calcYVel(self.game.elements.sprites()[0], self.game.elements.sprites()[1], self.y, self.x, "right")
                self.side = "left"
                #self.increaseSpeed(0.2)
                self.bounceCount += 1

    def calcYVel(self, player1, player2, bally, ballx, side):
        if side == "left":
            refPoint = player1.rect.center
            refPointx = refPoint[0] - player1.rect.height/2
            refPointy = refPoint[1]

            angle = ((bally + self.height/2) - refPointy) / (ballx - refPointx) * 45
            self.xVel += 0.2

            if angle < 0:
                angle = abs(angle)
                self.yVel = (math.tan(angle * (math.pi/180)) * abs(self.xVel)) * -1.2
            else:
                self.yVel = (math.tan(angle * (math.pi/180)) * abs(self.xVel)) * 1.2    

        if side == "right":
            refPoint = player2.rect.center
            refPointx = refPoint[0] + player2.rect.height/2
            refPointy = refPoint[1]

            angle = ((bally + self.height/2) - refPointy) / (ballx - refPointx) * 45
            self.xVel -= 0.2

            if angle < 0:
                angle = abs(angle)
                self.yVel = (math.tan(angle * (math.pi/180)) * abs(self.xVel)) * 1.2
            else:
                self.yVel = (math.tan(angle * (math.pi/180)) * abs(self.xVel)) * -1.2          

    def update(self):
        self.checkWalls()
        self.y += self.yVel
        self.rect.y = self.y
        self.x += self.xVel
        self.rect.x = self.x
        