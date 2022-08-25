##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

import pygame
import sys
from settings import *
from elements import *

class Menu:
    def __init__(self):
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def setup(self):
        self.elements = pygame.sprite.Group()

        self.particleSpawner = ParticleSpawner()

        gameFont5x5small = pygame.font.Font("bit5x5.ttf", 32)
        gameFont5x5large = pygame.font.Font("bit5x5.ttf", 124)

        self.widthAdj = 50
        self.heightAdj = -175
        self.heightAnimationPong = 350
        self.heightAnimationGame = 350
        self.sideAnimationUntitled = 480

        self.textUntitled = gameFont5x5small.render("untitled", False, LIGHTGREY)
        self.textUntitledRect = self.textUntitled.get_rect(center = (WIDTH/2 - 180 + self.widthAdj - self.sideAnimationUntitled, HEIGHT/2 - 100 + self.heightAdj))

        self.textPong = gameFont5x5large.render("pong", False, LIGHTGREY)
        self.textPongRect = self.textPong.get_rect(center = (WIDTH/2 - 90 + self.widthAdj, HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong))

        self.textGame = gameFont5x5large.render("game", False, LIGHTGREY)
        self.textGameRect = self.textGame.get_rect(center = (WIDTH/2 + 2 + self.widthAdj, HEIGHT/2 + 65 + self.heightAdj - self.heightAnimationGame))

        self.playButton = gameFont5x5small.render("Play", False, LIGHTGREY)
        self.playButtonRect = self.playButton.get_rect(center = (WIDTH/2, HEIGHT/2 + 100))

        self.settingsButton = gameFont5x5small.render("Settings", False, LIGHTGREY)
        self.settingsButtonRect = self.settingsButton.get_rect(center = (WIDTH/2, HEIGHT/2 + 175))

        self.creditsButton = gameFont5x5small.render("Credits", False, LIGHTGREY)
        self.creditsButtonRect = self.creditsButton.get_rect(center = (WIDTH/2, HEIGHT/2 + 250))

        self.player1menu = Player(self, WIDTH/2 + self.playButtonRect.width * 1.5 - 7, self.playButtonRect.y - self.playButtonRect.height/2, WIDTH/100, HEIGHT/15, "menu1")
        self.player2menu = Player(self, WIDTH/2 - self.playButtonRect.width * 1.5 - 7, self.playButtonRect.y - self.playButtonRect.height/2, WIDTH/100, HEIGHT/15, "menu2")

        self.cover = pygame.Surface([WIDTH, HEIGHT* 0.6])
        self.cover.fill(DARKGREY)
        self.coverRect = self.cover.get_rect(center = (WIDTH/2, HEIGHT/2 + 200))

        self.draw()

    def draw(self):
        self.screen.fill(DARKGREY)
        self.elements.draw(self.screen)

        self.screen.blit(self.textUntitled, self.textUntitledRect)
        self.screen.blit(self.textPong, self.textPongRect)
        self.screen.blit(self.textGame, self.textGameRect)

        self.screen.blit(self.playButton, self.playButtonRect)
        self.screen.blit(self.settingsButton, self.settingsButtonRect)
        self.screen.blit(self.creditsButton, self.creditsButtonRect)

        self.screen.blit(self.cover, self.coverRect)

        self.particleSpawner.particleGroup.draw(self.screen)
        pygame.display.flip()

    def run(self):
        self.menuOpen = True
        self.counter = 0
        self.placement = self.playButtonRect.y - self.playButtonRect.height/2

        gameFont5x5small = pygame.font.Font("bit5x5.ttf", 32)
        while self.menuOpen:
            self.tickspeed = self.clock.tick(FPS) / 1000.0
            self.elements.update()

            self.counter += self.tickspeed
            if self.counter > 2.7:
                self.alpha = 255 / (self.counter - 2.5/1)
                self.cover.set_alpha(self.alpha)
            elif self.counter > 2.4:
                if self.heightAnimationGame > 0:
                    self.heightAnimationGame -= 50
                    self.textGameRect = self.textGame.get_rect(center = (WIDTH/2 + 2 + self.widthAdj, HEIGHT/2 + 65 + self.heightAdj - self.heightAnimationGame))
                    if self.heightAnimationGame == 0:
                        for i in range(15):
                            self.particleSpawner.spawnParticles(LIGHTGREY, WIDTH/2 + 2 + self.widthAdj + random.uniform(-150, 150), HEIGHT/2 + 65 + self.heightAdj - self.heightAnimationGame + 30, "title")
            if self.counter > 2.0:
                if self.heightAnimationPong > 0:
                    self.heightAnimationPong -= 50
                    self.textPongRect = self.textPong.get_rect(center = (WIDTH/2 - 90 + self.widthAdj, HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong))
                    if self.heightAnimationPong == 0:
                        for i in range(15):
                           self.particleSpawner.spawnParticles(LIGHTGREY, WIDTH/2 - 90 + self.widthAdj + random.uniform(-150, 150), HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong + 30, "title") 
            elif self.counter > 0.6:
                if self.sideAnimationUntitled > 0:
                    self.sideAnimationUntitled -= 10
                    self.textUntitledRect = self.textUntitled.get_rect(center = (WIDTH/2 - 180 + self.widthAdj - self.sideAnimationUntitled, HEIGHT/2 - 100 + self.heightAdj))
            
            if self.counter > 3:
                mousePos = pygame.mouse.get_pos()
                if self.playButtonRect.collidepoint(mousePos):
                    self.playButton = gameFont5x5small.render("Play", False, LIGHTLIGHTGREY)
                    self.placement = self.playButtonRect.y - self.playButtonRect.height/2
                else:
                    self.playButton = gameFont5x5small.render("Play", False, LIGHTGREY)

                if self.settingsButtonRect.collidepoint(mousePos):
                    self.settingsButton = gameFont5x5small.render("Settings", False, LIGHTLIGHTGREY)
                    self.placement = self.settingsButtonRect.y - self.settingsButtonRect.height/2
                else:
                    self.settingsButton = gameFont5x5small.render("Settings", False, LIGHTGREY)

                if self.creditsButtonRect.collidepoint(mousePos):
                    self.creditsButton = gameFont5x5small.render("Credits", False, LIGHTLIGHTGREY)
                    self.placement = self.creditsButtonRect.y - self.creditsButtonRect.height/2
                else:
                    self.creditsButton = gameFont5x5small.render("Credits", False, LIGHTGREY)

                if self.player1menu.y != self.placement:
                    if self.player1menu.y > self.placement:
                        self.player1menu.velocity = -50 * (abs(self.player1menu.y - self.placement)/self.placement)
                    elif self.player1menu.y < self.placement:
                        self.player1menu.velocity = 50 * (abs(self.player1menu.y - self.placement)/self.placement)

                if self.player2menu.y != self.placement:
                    if self.player2menu.y > self.placement:
                        self.player2menu.velocity = -50 * (abs(self.player2menu.y - self.placement)/self.placement)
                    elif self.player2menu.y < self.placement:
                        self.player2menu.velocity = 50 * (abs(self.player2menu.y - self.placement)/self.placement)

            self.draw()
            self.particleSpawner.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()