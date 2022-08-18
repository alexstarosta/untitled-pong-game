##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

import pygame
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
        self.groups = game.elements
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([bwidth, bheight])
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.width = bwidth
        self.height = bheight
        self.xVel = xVel
        self.yVel = yVel
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.x = x

    def checkWalls(self):
        if self.y < 0 or self.y > HEIGHT - self.height:
            print("height")
            self.yVel *= -1
        if self.x < 0 or self.x > WIDTH - self.width:
            print("width")
            self.xVel *= -1

    def update(self):
        self.checkWalls()
        self.y += self.yVel
        self.rect.y = self.y
        self.x += self.xVel
        self.rect.x = self.x
        