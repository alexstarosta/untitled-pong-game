##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

from os import kill
import pygame
import math
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, pwidth, pheight, player, gamemode):
        self.groups = game.elements
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([pwidth, pheight])
        if player == 1 or player == "menu1":
            self.image.fill(BLUE)
        elif player == 2 or player == "menu2":
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.velocity = 0
        self.direction = "none"
        self.height = pheight
        self.player = player
        self.gamemode = gamemode
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.up = False
        self.down = False

    def getInput(self):
        if self.player == 1:
            if self.gamemode == "bot 1v1":
                if self.up:
                    self.velocity = -PADDLE_SPEED
                    self.direction = "up"
                if self.down:
                    self.velocity = PADDLE_SPEED
                    self.direction = "down"
                if self.velocity != 0: 
                    self.velocity *= 0.7
            else:
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
            if self.gamemode == "1 player" or self.gamemode == "bot 1v1":
                if self.up:
                    self.velocity = -PADDLE_SPEED
                    self.direction = "up"
                if self.down:
                    self.velocity = PADDLE_SPEED
                    self.direction = "down"
                if self.velocity != 0: 
                    self.velocity *= 0.7
            else:
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
    def __init__(self, game, x, y, xVel, yVel, bwidth, bheight, color):
        self.groups = game.ballElements
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([bwidth, bheight])
        self.image.fill(color)
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
        self.angle = 0
        self.lastWinner = "unknown"

    def startGame(self):
        self.startBall(self.prexVel,self.preyVel)

    def startBall(self, xVel, yVel):
        if self.lastWinner == "right":
            self.xVel = -abs(xVel)
        else:
            self.xVel = abs(xVel)
        self.yVel = yVel

    def resetBall(self):
        self.bounceCount = 0
        self.y = self.originy
        self.x = self.originx
        self.rect.x = self.originx
        self.rect.y = self.originy
        self.yVel = 0
        self.xVel = 0
        self.side = "unknown"

    def increaseSpeed(self, amount):
        if self.xVel > 0.01:
            self.xVel += amount
        else:
            self.xVel -= amount

    def checkWalls(self):
        if self.y < 0 or self.y > HEIGHT - self.height:
            self.yVel *= -1
        if self.x < 0:
            self.resetBall()
            self.game.gameState = "playing"
            self.game.gameCountdown = 5
            self.game.score[1] += 1
            self.lastWinner = "right"
            self.game.drawScores()
        elif self.x > WIDTH - self.width:
            self.resetBall()
            self.game.gameState = "playing"
            self.game.gameCountdown = 5
            self.game.score[0] += 1
            self.lastWinner = "left"
            self.game.drawScores()
        if self.x < WIDTH/2 and pygame.sprite.spritecollideany(self, self.game.elements):
            self.xVel = abs(self.xVel)
            if self.side == "unknown" or self.side == "left":
                self.calcYVel(self.game.elements.sprites()[0], self.game.elements.sprites()[1], self.y, self.x, "left")
                if hasattr(self.game, 'particleSpawner'):
                    if self.angle > 41 or self.angle < -41:
                        self.game.particleSpawner.spawnParticles(BLUE, self.rect.x, self.y, "corner")
                    else:
                        self.game.particleSpawner.spawnParticles(BLUE, self.game.elements.sprites()[0].rect.right, self.y, "left")
                self.side = "right"
                self.increaseSpeed(0.4)
                self.bounceCount += 1
        if self.x > WIDTH/2 and pygame.sprite.spritecollideany(self, self.game.elements):
            self.xVel = -abs(self.xVel)
            if self.side == "unknown" or self.side == "right":
                self.calcYVel(self.game.elements.sprites()[0], self.game.elements.sprites()[1], self.y, self.x, "right")
                if hasattr(self.game, 'particleSpawner'):
                    if self.angle > 41 or self.angle < -41:
                        self.game.particleSpawner.spawnParticles(RED, self.rect.x, self.y, "corner")
                    else:
                        self.game.particleSpawner.spawnParticles(RED, self.game.elements.sprites()[1].rect.left, self.y, "right")
                self.side = "left"
                self.increaseSpeed(0.4)
                self.bounceCount += 1

    def calcYVel(self, player1, player2, bally, ballx, side):
        if side == "left":
            refPoint = player1.rect.center
            refPointx = refPoint[0] - player1.rect.height/2
            refPointy = refPoint[1]

            self.angle = ((bally + self.height/2) - refPointy) / (ballx - refPointx) * 45

            if self.angle > 65:
                self.angle = 65
            elif self.angle < -65:
                self.angle = -65

            self.xVel -= 0.2

            if self.angle < 0:
                self.angle = abs(self.angle)
                self.yVel = (math.tan(self.angle * (math.pi/180)) * abs(self.xVel)) * -1.2
            else:
                self.yVel = (math.tan(self.angle * (math.pi/180)) * abs(self.xVel)) * 1.2    

        if side == "right":
            refPoint = player2.rect.center
            refPointx = refPoint[0] + player2.rect.height/2
            refPointy = refPoint[1]

            self.angle = ((bally + self.height/2) - refPointy) / ((ballx + self.width) - refPointx) * 45

            if self.angle > 65:
                self.angle = 65
            elif self.angle < -65:
                self.angle = -65

            self.xVel -= 0.2

            if self.angle < 0:
                self.angle = abs(self.angle)
                self.yVel = (math.tan(self.angle * (math.pi/180)) * abs(self.xVel)) * 1.2
            else:
                self.yVel = (math.tan(self.angle * (math.pi/180)) * abs(self.xVel)) * -1.2          

    def update(self):
        self.checkWalls()
        self.y += self.yVel
        self.rect.y = self.y
        self.x += self.xVel
        self.rect.x = self.x

class Particle(pygame.sprite.Sprite):
    def __init__(self, color, position):
        super(Particle, self).__init__()
        if position == "title":
            self.width = random.randrange(15,19)*1.25
        else:
            self.width = random.randrange(15,19)
        self.originWidth = self.width
        self.height = self.width
        self.size = (self.width, self.height)
        self.image = pygame.Surface(self.size)
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        if position == "right":
            self.xVel = random.uniform(-8, 0)
        if position == "left":
            self.xVel = random.uniform(0, 8)
        if position == "corner" or position == "title":
            self.xVel = random.uniform(-8, 8)
        if position == "title":
            self.yVel = random.uniform(0, 8)
        else:
            self.yVel = random.uniform(-8, 8)
        if position == "title":
            self.killTimer = random.randint(10,12)*2
        else:
            self.killTimer = random.randint(10,15)
        self.startTimer = self.killTimer
        self.updateCount = 0
        
    def update(self):
        if self.updateCount % 3 != 0:
            self.rect.x += self.xVel
            self.rect.y += self.yVel
            if self.killTimer == 0:
                self.kill()
            else:
                self.killTimer -= 1
            self.width = math.ceil((self.killTimer/self.startTimer) * self.originWidth)
            self.height = self.width
            self.size = (self.width, self.height)
            self.image = pygame.Surface(self.size)
            self.image.fill(self.color)
            self.updateCount += 1
        else:
            self.updateCount += 1

class ParticleSpawner:
    def __init__(self):
        self.particleGroup = pygame.sprite.Group()

    def update(self):
        self.particleGroup.update()

    def spawnParticles(self, color, x, y, position):
        particleAmount = random.randrange(5,9)
        for i in range(particleAmount):
            particle = Particle(color, position)
            particle.rect.x = x
            particle.rect.y = y
            self.particleGroup.add(particle)

class KeybindChecker(pygame.sprite.Sprite):
    def __init__(self, game, key, x, y, length, width, color):
        self.groups = game.ballElements
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([length, width])
        self.image.fill(color)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.key = key
        self.clicked = False
        self.fadeIn = False
        self.hidden = False
        self.clock = pygame.time.Clock()
        self.counter = 0

    def easeOutQuad(self, num):
        return 1 - (1 - num) * (1 - num)

    def hide(self):
        self.hidden = True
        self.image.set_alpha(0)

    def update(self):
        if self.hidden == False:
            self.tickspeed = self.clock.tick(FPS) / 1000.0
            if self.fadeIn:
                self.counter += self.tickspeed * 2
                self.alpha = 255 * self.easeOutQuad(self.counter) + 100
                self.image.set_alpha(self.alpha)
                if self.alpha >= 254:
                    self.fadeIn = False

            keys = pygame.key.get_pressed()
            if self.key == "w":
                if keys[pygame.K_w]:
                    self.counter = 0
                    self.fadeIn = True
                    self.clicked = True
            if self.key == "s":
                if keys[pygame.K_s]:
                    self.counter = 0
                    self.fadeIn = True
                    self.clicked = True
            if self.key == "d":
                if keys[pygame.K_d]:
                    self.counter = 0
                    self.fadeIn = True
                    self.clicked = True
            if self.key == "up":
                if keys[pygame.K_UP]:
                    self.counter = 0
                    self.fadeIn = True
                    self.clicked = True
            if self.key == "down":
                if keys[pygame.K_DOWN]:
                    self.counter = 0
                    self.fadeIn = True
                    self.clicked = True
            if self.key == "left":
                if keys[pygame.K_LEFT]:
                    self.counter = 0
                    self.fadeIn = True
                    self.clicked = True
