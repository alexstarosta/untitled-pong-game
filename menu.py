##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

import pygame
import sys
from settings import *
from elements import *
from game import *

# starting game function
def startGame(gamemode, sfx, particle):
    from game import Game
    gamestate = "inactive"
    game = Game(gamestate, gamemode, sfx, particle)
    game.setup()
    game.run()

def updateValues(sfx, particles, gamemode):
    import settings
    settings.SFX = sfx
    settings.PARTICLES = particles
    settings.GAMEMODE = gamemode

class Menu:
    def __init__(self, sfx, particle, gamemode, speed):
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.optionsOpen = False
        self.creditsOpen = False
        self.sfxSetting = sfx
        self.particleSetting = particle
        self.gamemode = gamemode
        self.speed = speed
        self.alpha = 255
        self.oclick = 0
        self.ofall = False
        self.ofallspeed = 0
        self.randomfactor = random.uniform(-20,20)

    def setup(self):
        self.elements = pygame.sprite.Group()

        self.particleSpawner = ParticleSpawner()

        gameFont5x5small = pygame.font.Font("assets/bit5x5.ttf", 32)
        gameFont5x5smallsmall = pygame.font.Font("assets/bit5x5.ttf", 22)
        gameFont5x5large = pygame.font.Font("assets/bit5x5.ttf", 124)

        self.widthAdj = 50
        self.heightAdj = -175
        self.heightAnimationPong = 300
        self.heightAnimationGame = 350
        self.sideAnimationUntitled = 480

        self.textUntitled = gameFont5x5small.render("untitled", False, LIGHTGREY)
        self.textUntitledRect = self.textUntitled.get_rect(center = (WIDTH/2 - 180 + self.widthAdj - self.sideAnimationUntitled, HEIGHT/2 - 100 + self.heightAdj))

        self.textPong = gameFont5x5large.render("p   ng", False, LIGHTGREY)
        self.textPongRect = self.textPong.get_rect(center = (WIDTH/2 - 90 + self.widthAdj, HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong))

        self.texto = gameFont5x5large.render("o", False, LIGHTGREY)
        self.textoRect = self.texto.get_rect(center = (WIDTH/2 - 190 + self.widthAdj, HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong))

        self.textGame = gameFont5x5large.render("game", False, LIGHTGREY)
        self.textGameRect = self.textGame.get_rect(center = (WIDTH/2 + 2 + self.widthAdj, HEIGHT/2 + 65 + self.heightAdj - self.heightAnimationGame))

        self.playButton = gameFont5x5small.render("Play", False, LIGHTGREY)
        self.playButtonRect = self.playButton.get_rect(center = (WIDTH/2, HEIGHT/2 + 100))

        self.optionsButton = gameFont5x5small.render("options", False, LIGHTGREY)
        self.optionsButtonRect = self.optionsButton.get_rect(center = (WIDTH/2, HEIGHT/2 + 175))

        self.creditsButton = gameFont5x5small.render("Credits", False, LIGHTGREY)
        self.creditsButtonRect = self.creditsButton.get_rect(center = (WIDTH/2, HEIGHT/2 + 250))
        
        self.player1menu = Player(self, WIDTH/2 + self.playButtonRect.width * 1.5 - 7, self.playButtonRect.y - self.playButtonRect.height/2, WIDTH/100, HEIGHT/15, "menu1", "2 player")
        self.player2menu = Player(self, WIDTH/2 - self.playButtonRect.width * 1.5 - 7, self.playButtonRect.y - self.playButtonRect.height/2, WIDTH/100, HEIGHT/15, "menu2", "2 player")

        if self.speed != "fast":
            self.cover = pygame.Surface([WIDTH, HEIGHT* 0.6])
            self.cover.fill(DARKGREY)
            self.coverRect = self.cover.get_rect(center = (WIDTH/2, HEIGHT/2 + 200))
        else:
            self.cover = pygame.Surface([WIDTH, HEIGHT])
            self.cover.fill(DARKGREY)
            self.coverRect = self.cover.get_rect(center = (WIDTH/2, HEIGHT/2))

        self.draw()

    def draw(self):
        import settings
        if settings.EGG:
            self.alpha = 0
            self.screen.fill(WHITE)
            cellSize = round(WIDTH/40)
            count = 0
            for x in range(round(WIDTH/20)):
                for y in range(round(WIDTH/20)):
                    if count%2 == 0:
                        pygame.draw.rect(self.screen, (230,230,230), (x*cellSize + self.counter*20%round(WIDTH/40) + self.randomfactor - 100, y*cellSize + self.counter*20%round(WIDTH/40) - 100, cellSize, cellSize))
                    count += 1
        else:
            self.screen.fill(DARKGREY)
        self.elements.draw(self.screen)

        self.screen.blit(self.textUntitled, self.textUntitledRect)
        self.screen.blit(self.textPong, self.textPongRect)
        self.screen.blit(self.texto, self.textoRect)
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

        if self.creditsOpen:
            self.screen.blit(self.credit1, self.credit1Rect)
            self.screen.blit(self.credit2, self.credit2Rect)
            self.screen.blit(self.credit11, self.credit11Rect)
            self.screen.blit(self.credit22, self.credit22Rect)
        
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
            gameFont5x5small = pygame.font.Font("assets/bit5x5.ttf", 32)

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
            self.optionsOpen = False
            self.updateMenuItems(0)

    def setupCredits(self, state):
        if state == "open":
            gameFont5x5small = pygame.font.Font("assets/bit5x5.ttf", 32)
            gameFont5x5smallsmall = pygame.font.Font("assets/bit5x5.ttf", 26)

            self.credit1 = gameFont5x5smallsmall.render("a Game by", False, LIGHTGREY)
            self.credit1Rect = self.credit1.get_rect(midleft = (WIDTH/2 - 50, HEIGHT/2 + 100))

            self.credit11 = gameFont5x5small.render("Alex Starosta", False, LIGHTGREY)
            self.credit11Rect = self.credit11.get_rect(midleft = (WIDTH/2 - 50, HEIGHT/2 + 140))

            self.credit2 = gameFont5x5smallsmall.render("Bitfonts by", False, LIGHTGREY)
            self.credit2Rect = self.credit2.get_rect(midleft = (WIDTH/2 - 50, HEIGHT/2 + 215))

            self.credit22 = gameFont5x5small.render("Matt LaGrandeur", False, LIGHTGREY)
            self.credit22Rect = self.credit22.get_rect(midleft = (WIDTH/2 - 50, HEIGHT/2 + 255))

            self.updateMenuItems(-255)

            self.creditsOpen = True
            pygame.display.flip()
        elif state == "close":
            self.creditsOpen = False
            self.updateMenuItems(0)

    def reRenderSettings(self):
        gameFont5x5small = pygame.font.Font("assets/bit5x5.ttf", 32)

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

        gameFont5x5small = pygame.font.Font("assets/bit5x5.ttf", 32)
        while self.menuOpen:
            self.tickspeed = self.clock.tick(FPS) / 1000
            self.elements.update()

            if self.speed == "fast":
                self.heightAnimationPong = 0
                self.heightAnimationGame = 0
                self.sideAnimationUntitled = 0

            self.counter += self.tickspeed*2

            if self.alpha != 0:
                if self.speed != "fast":
                    if self.counter > 2.5:
                        self.alpha = 255 / (round(self.counter,1) - 2.4)
                        self.cover.set_alpha(self.alpha)
                else:
                    if self.counter > 0.5:
                        self.alpha = 255 / (round(self.counter,1) - 0.4)
                        self.cover.set_alpha(self.alpha)
            else:
                self.cover.set_alpha(self.alpha)

            if self.speed != "fast":
                if self.counter > 2.1:
                    if self.heightAnimationGame > 0:
                        self.heightAnimationGame -= 50
                        self.textGameRect = self.textGame.get_rect(center = (WIDTH/2 + 2 + self.widthAdj, HEIGHT/2 + 65 + self.heightAdj - self.heightAnimationGame))
                        if self.heightAnimationGame == 0:
                            for i in range(25):
                                self.particleSpawner.spawnParticles(LIGHTGREY, WIDTH/2 + 2 + self.widthAdj + random.uniform(-150, 150), HEIGHT/2 + 65 + self.heightAdj - self.heightAnimationGame + 30, "title")
                if self.counter > 1.7:
                    if self.heightAnimationPong > 0:
                        self.heightAnimationPong -= 50
                        self.textPongRect = self.textPong.get_rect(center = (WIDTH/2 - 90 + self.widthAdj, HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong))
                        self.textoRect = self.texto.get_rect(center = (WIDTH/2 - 138 + self.widthAdj, HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong))
                        if self.heightAnimationPong == 0:
                            for i in range(25):
                                self.particleSpawner.spawnParticles(LIGHTGREY, WIDTH/2 - 90 + self.widthAdj + random.uniform(-150, 150), HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong + 20, "title") 
                if self.counter > 0.6:
                    if self.sideAnimationUntitled > 0:
                        self.sideAnimationUntitled -= 20
                        self.textUntitledRect = self.textUntitled.get_rect(center = (WIDTH/2 - 180 + self.widthAdj - self.sideAnimationUntitled, HEIGHT/2 - 100 + self.heightAdj))
            else:
                if self.counter < 0.1:
                    self.textGameRect = self.textGame.get_rect(center = (WIDTH/2 + 2 + self.widthAdj, HEIGHT/2 + 65 + self.heightAdj - self.heightAnimationGame))
                    self.textPongRect = self.textPong.get_rect(center = (WIDTH/2 - 90 + self.widthAdj, HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong))
                    self.textoRect = self.texto.get_rect(center = (WIDTH/2 - 138 + self.widthAdj, HEIGHT/2 - 30 + self.heightAdj - self.heightAnimationPong))
                    self.textUntitledRect = self.textUntitled.get_rect(center = (WIDTH/2 - 180 + self.widthAdj - self.sideAnimationUntitled, HEIGHT/2 - 100 + self.heightAdj))

            if self.ofall:
                self.ofallspeed += 0.5
                self.textoRect.y += self.ofallspeed
                if self.textoRect.y > 1000:
                    self.ofall = False
                    import settings
                    settings.EGG = True

            if self.counter > 3 or self.speed == "fast" and self.counter > 1.5:
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
                            updateValues(self.sfxSetting, self.particleSetting, self.gamemode)
                            startGame(self.gamemode, self.sfxSetting, self.particleSetting)
                        elif self.optionsButtonRect.collidepoint(mousePos):
                                if self.optionsOpen:
                                    self.setupOptions("close")
                                else:
                                    self.setupCredits("close")
                                    self.setupOptions("open")
                        elif self.creditsButtonRect.collidepoint(mousePos):
                                if self.creditsOpen:
                                    self.setupCredits("close")
                                else:
                                    self.setupOptions("close")
                                    self.setupCredits("open")

                        if self.textoRect.collidepoint(mousePos):
                            self.oclick += 1
                            self.particleSpawner.spawnParticles(LIGHTGREY, mousePos[0], mousePos[1], "fire")
                            if self.oclick > 2:
                                self.ofall = True
                            else:
                                self.textoRect.y += 5

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