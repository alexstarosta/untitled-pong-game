##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

from pickle import REDUCE
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
        self.optionsOpen = False
        self.sfxSetting = "on"
        self.particleSetting = "on"
        self.gamemode = "1 player"

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

        self.optionsButton = gameFont5x5small.render("options", False, LIGHTGREY)
        self.optionsButtonRect = self.optionsButton.get_rect(center = (WIDTH/2, HEIGHT/2 + 175))

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
        self.screen.blit(self.optionsButton, self.optionsButtonRect)
        self.screen.blit(self.creditsButton, self.creditsButtonRect)

        self.screen.blit(self.cover, self.coverRect)

        if self.optionsOpen:
            self.screen.blit(self.modeButton, self.modeButtonRect)
            self.screen.blit(self.sfxButton, self.sfxButtonRect)
            self.screen.blit(self.partiButton, self.partiButtonRect)
            self.screen.blit(self.sfxButtonAction, self.sfxButtonActionRect)
            self.screen.blit(self.partiButtonAction, self.partiButtonActionRect)
            self.screen.blit(self.modeButtonAction, self.modeButtonActionRect)

        self.particleSpawner.particleGroup.draw(self.screen)
        pygame.display.flip()

    def updateMenuItems(self, adj):
        self.playButtonRect = self.playButton.get_rect(center = (WIDTH/2 + adj, HEIGHT/2 + 100))

        self.optionsButtonRect = self.optionsButton.get_rect(center = (WIDTH/2 + adj, HEIGHT/2 + 175))

        self.creditsButtonRect = self.creditsButton.get_rect(center = (WIDTH/2 + adj, HEIGHT/2 + 250))

        self.player1menu.rect.x = WIDTH/2 + self.playButtonRect.width * 1.5 - 7 + adj
        self.player2menu.rect.x = WIDTH/2 - self.playButtonRect.width * 1.5 - 7 + adj


    def setupOptions(self, state):
        if state == "open":
            gameFont5x5small = pygame.font.Font("bit5x5.ttf", 32)

            self.modeButton = gameFont5x5small.render("Mode:", False, LIGHTGREY)
            self.modeButtonRect = self.modeButton.get_rect(midright = (WIDTH/2 + 175, HEIGHT/2 + 100))

            self.modeButtonAction = gameFont5x5small.render(self.gamemode, False, LIGHTGREY)
            self.modeButtonActionRect = self.modeButtonAction.get_rect(midleft = (WIDTH/2 + 200, HEIGHT/2 + 100))

            self.sfxButton = gameFont5x5small.render("sfx:", False, LIGHTGREY)
            self.sfxButtonRect = self.sfxButton.get_rect(midright = (WIDTH/2 + 175, HEIGHT/2 + 175))

            self.sfxButtonAction = gameFont5x5small.render(self.sfxSetting, False, RED)
            self.sfxButtonActionRect = self.sfxButtonAction.get_rect(midleft = (WIDTH/2 + 200, HEIGHT/2 + 175))

            self.partiButton = gameFont5x5small.render("Particles:", False, LIGHTGREY)
            self.partiButtonRect = self.partiButton.get_rect(midright = (WIDTH/2 + 175, HEIGHT/2 + 250))

            self.partiButtonAction = gameFont5x5small.render(self.particleSetting, False, RED)
            self.partiButtonActionRect = self.partiButtonAction.get_rect(midleft = (WIDTH/2 + 200, HEIGHT/2 + 250))

            self.updateMenuItems(-255)

            self.optionsOpen = True
            pygame.display.flip()
        elif state == "close":
            gameFont5x5small = pygame.font.Font("bit5x5.ttf", 32)
            self.optionsOpen = False
            self.updateMenuItems(0)

    def reRenderSettings(self):
        gameFont5x5small = pygame.font.Font("bit5x5.ttf", 32)

        self.modeButtonAction = gameFont5x5small.render(self.gamemode, False, LIGHTGREY)

        if self.sfxSetting == "on":
            self.sfxButtonAction = gameFont5x5small.render(self.sfxSetting, False, RED)
        else:
            self.sfxButtonAction = gameFont5x5small.render(self.sfxSetting, False, BLUE)

        if self.particleSetting == "on":
            self.partiButtonAction = gameFont5x5small.render(self.particleSetting, False, RED)
        else:
            self.partiButtonAction = gameFont5x5small.render(self.particleSetting, False, BLUE)


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
                           self.particleSpawner.spawnParticles(LIGHTGREY, WIDTH/2 - 90 + self.widthAdj + random.uniform(-150, 150), HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong + 20, "title") 
            elif self.counter > 0.6:
                if self.sideAnimationUntitled > 0:
                    self.sideAnimationUntitled -= 10
                    self.textUntitledRect = self.textUntitled.get_rect(center = (WIDTH/2 - 180 + self.widthAdj - self.sideAnimationUntitled, HEIGHT/2 - 100 + self.heightAdj))
            
            if self.counter > 3:
                if not self.optionsOpen:
                    mousePos = pygame.mouse.get_pos()
                    if self.playButtonRect.collidepoint(mousePos):
                        self.playButton = gameFont5x5small.render("Play", False, LIGHTLIGHTGREY)
                        self.placement = self.playButtonRect.y - self.playButtonRect.height/2
                    else:
                        self.playButton = gameFont5x5small.render("Play", False, LIGHTGREY)

                    if self.optionsButtonRect.collidepoint(mousePos):
                        self.optionsButton = gameFont5x5small.render("options", False, LIGHTLIGHTGREY)
                        self.placement = self.optionsButtonRect.y - self.optionsButtonRect.height/2
                    else:
                        self.optionsButton = gameFont5x5small.render("options", False, LIGHTGREY)

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
                        self.player2menu.velocity = -75 * (abs(self.player2menu.y - self.placement)/self.placement)
                    elif self.player2menu.y < self.placement:
                        self.player2menu.velocity = 75 * (abs(self.player2menu.y - self.placement)/self.placement)

            if self.optionsOpen:
                mousePos = pygame.mouse.get_pos()
                if self.sfxButtonActionRect.collidepoint(mousePos):
                    if self.sfxSetting == "on":
                        self.sfxButtonAction = gameFont5x5small.render(self.sfxSetting, False, LIGHTRED)
                    else:
                        self.sfxButtonAction = gameFont5x5small.render(self.sfxSetting, False, LIGHTBLUE)
                else:
                    if self.sfxSetting == "on":
                        self.sfxButtonAction = gameFont5x5small.render(self.sfxSetting, False, RED)
                    else:
                        self.sfxButtonAction = gameFont5x5small.render(self.sfxSetting, False, BLUE)
                
                if self.partiButtonActionRect.collidepoint(mousePos):
                    if self.particleSetting == "on":
                        self.partiButtonAction = gameFont5x5small.render(self.particleSetting, False, LIGHTRED)
                    else:
                        self.partiButtonAction = gameFont5x5small.render(self.particleSetting, False, LIGHTBLUE)
                else:
                    if self.particleSetting == "on":
                        self.partiButtonAction = gameFont5x5small.render(self.particleSetting, False, RED)
                    else:
                        self.partiButtonAction = gameFont5x5small.render(self.particleSetting, False, BLUE)

                if self.modeButtonActionRect.collidepoint(mousePos):
                    self.modeButtonAction = gameFont5x5small.render(self.gamemode, False, LIGHTLIGHTGREY)
                else:
                    self.modeButtonAction = gameFont5x5small.render(self.gamemode, False, LIGHTGREY)




            self.draw()
            self.particleSpawner.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                if self.counter > 3:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.playButtonRect.collidepoint(mousePos):
                            if not self.optionsOpen:
                                print("play")
                        elif self.optionsButtonRect.collidepoint(mousePos):
                            if self.optionsOpen:
                                self.setupOptions("close")
                            else:
                                self.setupOptions("open")
                        elif self.creditsButtonRect.collidepoint(mousePos):
                            if not self.optionsOpen:
                                print("credits")

                        if self.optionsOpen:
                            if self.sfxButtonActionRect.collidepoint(mousePos):
                                if self.sfxSetting == "on":
                                    self.sfxSetting = "off"
                                else:
                                    self.sfxSetting = "on"
                            self.reRenderSettings()
                    
                            if self.partiButtonActionRect.collidepoint(mousePos):
                                if self.particleSetting == "on":
                                    self.particleSetting = "off"
                                else:
                                    self.particleSetting = "on"
                                    self.particleSpawner.spawnParticles(LIGHTRED, mousePos[0], mousePos[1], "corner")

                            self.reRenderSettings()

                            if self.modeButtonActionRect.collidepoint(mousePos):
                                if self.gamemode == "1 player":
                                    self.gamemode = "2 player"
                                elif self.gamemode == "2 player":
                                    self.gamemode = "bot 1v1"
                                elif self.gamemode == "bot 1v1":
                                    self.gamemode = "1 player"
                            self.reRenderSettings()
                    

    def quit(self):
        pygame.quit()
        sys.exit()