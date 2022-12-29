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
from menu import *

def changeColor(image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
        
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
    return finalImage

def backToMenu():
    from menu import Menu
    import settings
    settings.EGG = False
    menu = Menu(settings.SFX, settings.PARTICLES, settings.GAMEMODE, "fast")
    menu.setup()
    menu.run()
    
class Game:
    def __init__(self, gamestate, gamemode, sfx, particle):
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.gamemode = gamemode
        self.sfx = sfx
        self.particles = particle
        self.gamestate = gamestate
        if gamemode == "bot 1v1":
            self.leftReady = True
            self.leftUpdateTime = random.randint(2,12)
            self.leftRandomSpace = random.randint(0,10)
            self.leftTargeting = random.randint(0,20)
            self.leftCloseTargeting = random.randint(50,150)
        else:
            self.leftReady = False
        if gamemode == "1 player" or gamemode == "bot 1v1":
            self.rightReady = True
            self.rightUpdateTime = random.randint(2,12)
            self.rightRandomSpace = random.randint(0,10)
            self.rightTargeting = random.randint(20,50)
            self.rightCloseTargeting = random.randint(50,150)
        else:
            self.rightReady = False
        self.gameCountdown = 6
        self.score = [0,0]
        self.counter = 0
        self.lcountertime = 0
        self.rcountertime = 0
        self.firecounter = 0
        self.firechange = 0
        self.fireSizeToggle = True
        self.fireballActive = False
        self.coverAlpha = 0
        self.randomfactor = random.uniform(-20,20)

    def setup(self):

        self.elements = pygame.sprite.Group()
        self.ballElements = pygame.sprite.Group()

        if self.particles == "on":
            self.particleSpawner = ParticleSpawner()

        self.player1 = Player(self, WIDTH/50, HEIGHT/2 - HEIGHT/12, WIDTH/50, HEIGHT/6, 1, self.gamemode)
        self.player2 = Player(self, WIDTH - 2*WIDTH/50 + 1, HEIGHT/2 - HEIGHT/12, WIDTH/50, HEIGHT/6, 2, self.gamemode)

        self.fireball = Ball(self, WIDTH/2 - ((WIDTH/50)/2), HEIGHT/2, 1*BALL_SPEED, 0.0*BALL_SPEED, 0, 0, FIREORANGE, "fireball")

        self.ball = Ball(self, WIDTH/2 - ((WIDTH/50)/2), HEIGHT/2, -1*BALL_SPEED, 0.0*BALL_SPEED, WIDTH/50, WIDTH/50, LIGHTGREY, "ball")

        if not self.leftReady:
            self.wkeyCheck = KeybindChecker(self, "w", WIDTH/4 - 50, HEIGHT/3 - 170, 100, 100, DARKBLUE)
            self.skeyCheck = KeybindChecker(self, "s", WIDTH/4 - 50, HEIGHT/3 - 60, 100, 100, DARKBLUE)
            self.dkeyCheck = KeybindChecker(self, "d", WIDTH/4 + 60, HEIGHT/3 - 120, 100, 100, DARKBLUE)

            self.wsd1nonscaled = pygame.image.load("assets/wsd1.png")
            self.wsd1 = pygame.transform.scale(self.wsd1nonscaled, (220,220))
            self.wsd1Rect = self.wsd1.get_rect(center = (WIDTH/2 - 200,HEIGHT/4))

        if not self.rightReady:
            self.upkeyCheck = KeybindChecker(self, "up", WIDTH/2 + WIDTH/4 - 50, HEIGHT/3 - 170, 100, 100, DARKRED)
            self.downkeyCheck = KeybindChecker(self, "down", WIDTH/2 + WIDTH/4 - 50, HEIGHT/3 - 60, 100, 100, DARKRED)
            self.leftkeyCheck = KeybindChecker(self, "left", WIDTH/2 + WIDTH/4 - 160, HEIGHT/3 - 120, 100, 100, DARKRED)

            self.udl1nonscaled = pygame.image.load("assets/updownleft1.png")
            self.udl1 = pygame.transform.scale(self.udl1nonscaled, (220,220))
            self.udl1Rect = self.udl1.get_rect(center = (WIDTH/2 + 200,HEIGHT/4))

        gameFont5x5 = pygame.font.Font("assets/bit5x5.ttf", 172)
        self.startingText = gameFont5x5.render("", False, LIGHTGREY)
        self.startingTextRect = self.startingText.get_rect(center = (WIDTH/1.92 - ((WIDTH/50)/2), HEIGHT/4))

        gameFont5x3 = pygame.font.Font("assets/bit5x3.ttf", 112)
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
        import settings
        if settings.EGG:
            self.alpha = 0
            self.screen.fill(WHITE)
            cellSize = round(WIDTH/40)
            count = 0

            if self.fireballActive:
                tilecolor = (255,208,199)
                speed = 5
            else:
                tilecolor = (230,230,230)
                speed = 1
            for x in range(round(WIDTH/20)):
                for y in range(round(WIDTH/20)):
                    if count%2 == 0:
                        pygame.draw.rect(self.screen, tilecolor, (x*cellSize + self.counter*speed/2%round(WIDTH/40) + self.randomfactor - 100, y*cellSize + self.counter*speed/2%round(WIDTH/40) - 100, cellSize, cellSize))
                    count += 1
        else:
            self.screen.fill(DARKGREY)
        self.elements.draw(self.screen)
        self.ballElements.draw(self.screen)
        self.screen.blit(self.startingText, self.startingTextRect)
        self.screen.blit(self.score1, self.score1Rect)
        self.screen.blit(self.score2, self.score2Rect)

        if self.coverAlpha != 0:
            self.screen.blit(self.cover, self.coverRect)
            self.screen.blit(self.gameover, self.gameoverRect)
            self.screen.blit(self.playagain, self.playagainRect)
            self.screen.blit(self.returntomenu, self.returntomenuRect)

        def changeColorGradient(c1, c2, count, type):
            if count > 50:
                if type == "fire":
                    self.firecounter = 0
                    if self.firechange == 0:
                        self.firechange = 1
                    elif self.firechange == 1:
                        self.firechange = 2
                    elif self.firechange == 2:
                        self.firechange = 0
                return c2
            rchange = (c2[0] - c1[0]) / 50
            gchange = (c2[1] - c1[1]) / 50
            bchange = (c2[2] - c1[2]) / 50
            return pygame.Color((int)(round(c1[0] + rchange*count)), (int)(round(c1[1] + gchange*count)),(int)(round(c1[2] + bchange*count)))

        if self.fireballActive:
            if self.fireSizeToggle:
                self.fireball.width += 1
                self.fireball.height += 1
                if self.fireball.width > WIDTH/30 + 5:
                    self.fireSizeToggle = not self.fireSizeToggle
            else:
                self.fireball.width -= 1
                self.fireball.height -= 1
                if self.fireball.width < WIDTH/30 - 5:
                    self.fireSizeToggle = not self.fireSizeToggle
            self.fireball.image = pygame.Surface([self.fireball.width, self.fireball.height])
            self.fireball.rect = self.fireball.image.get_rect(center = (self.ball.x + self.ball.width/2 - 1 + random.uniform(-5,5), self.ball.y + self.ball.height/2 - 1 + random.uniform(-5,5)))
        else:
            self.fireball.image = pygame.Surface([0, 0])
            self.fireball.rect = self.fireball.image.get_rect(center = (self.ball.x + self.ball.width/2 - 1 + random.uniform(-5,5), self.ball.y + self.ball.height/2 - 1 + random.uniform(-5,5)))

        if self.firechange == 0:
            if self.firecounter == 0:
                self.firecounter = self.counter
            self.fireball.image.fill(changeColorGradient(FIREORANGE, FIRERED, self.counter - self.firecounter, "fire"))
            self.fireball.color = changeColorGradient(FIREORANGE, FIRERED, self.counter - self.firecounter, "fire")
        elif self.firechange == 1:
            if self.firecounter == 0:
                self.firecounter = self.counter
            self.fireball.image.fill(changeColorGradient(FIRERED, FIREYELLOW, self.counter - self.firecounter, "fire"))
            self.fireball.color = changeColorGradient(FIRERED, FIREYELLOW, self.counter - self.firecounter, "fire")
        elif self.firechange == 2:
            if self.firecounter == 0:
                self.firecounter = self.counter
            self.fireball.image.fill(changeColorGradient(FIREYELLOW, FIREORANGE, self.counter - self.firecounter, "fire"))
            self.fireball.color = changeColorGradient(FIREYELLOW, FIREORANGE, self.counter - self.firecounter, "fire")

        if self.gamemode == "2 player" or self.gamemode == "1 player":
            if self.leftReady:
                if self.wsd1.get_alpha != 0:
                    if self.lcountertime == 0:
                        self.lcountertime = self.counter
                    self.screen.blit(changeColor(self.wsd1, changeColorGradient(LIGHTGREY, BLUE, self.counter - self.lcountertime, "key")), self.wsd1Rect)
            else:
                self.screen.blit(changeColor(self.wsd1, LIGHTGREY), self.wsd1Rect)

        if self.gamemode == "2 player":
            if self.rightReady:
                if self.udl1.get_alpha != 0:
                    if self.rcountertime == 0:
                        self.rcountertime = self.counter
                    self.screen.blit(changeColor(self.udl1, changeColorGradient(LIGHTGREY, RED, self.counter - self.rcountertime, "key")), self.udl1Rect)
            else:
                self.screen.blit(changeColor(self.udl1, LIGHTGREY), self.udl1Rect)
        
        if self.particles == "on":
            self.particleSpawner.particleGroup.draw(self.screen)
        pygame.display.flip()

    def drawCountdown(self, text):
        gameFont = pygame.font.Font("assets/bit5x5.ttf", 172)
        self.startingText = gameFont.render(f"{text}", False, LIGHTGREY)
        self.startingTextRect = self.startingText.get_rect(center = (WIDTH/1.92 - ((WIDTH/50)/2), HEIGHT/4))

        self.screen.blit(self.startingText, self.startingTextRect)
        pygame.display.flip() 

    def hidekeybinds(self):
        if self.gamemode == "2 player":
            self.udl1.set_alpha(0)
            self.upkeyCheck.hide()
            self.downkeyCheck.hide()
            self.leftkeyCheck.hide()

        if self.gamemode == "2 player" or self.gamemode == "1 player":
            self.wsd1.set_alpha(0)
            self.wkeyCheck.hide()
            self.skeyCheck.hide()
            self.dkeyCheck.hide()

    def drawScores(self):
        gameFont5x3 = pygame.font.Font("assets/bit5x3.ttf", 112)
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

    def endSequence(self):

        gameFont5x5 = pygame.font.Font("assets/bit5x5.ttf", 100)
        gameFont5x5small = pygame.font.Font("assets/bit5x5.ttf", 30)

        self.cover = pygame.Surface([WIDTH, HEIGHT])
        self.cover.fill(DARKGREY)
        self.coverRect = self.cover.get_rect(center = (WIDTH/2, HEIGHT/2))
        
        import settings
        if settings.EGG:
            self.gameover = gameFont5x5.render("Game Over", False, WHITE)
            self.playagain = gameFont5x5small.render("Play Again", False, WHITE)
            self.returntomenu = gameFont5x5small.render("Return to Menu", False, WHITE)
        else:
            self.gameover = gameFont5x5.render("Game Over", False, LIGHTGREY)
            self.playagain = gameFont5x5small.render("Play Again", False, LIGHTGREY)
            self.returntomenu = gameFont5x5small.render("Return to Menu", False, LIGHTGREY)

        self.gameoverRect = self.gameover.get_rect(center = (WIDTH/2, HEIGHT/2.5))
        self.playagainRect = self.playagain.get_rect(midright = (WIDTH/2 - 70, HEIGHT/1.75))
        self.returntomenuRect = self.returntomenu.get_rect(midleft = (WIDTH/2 - 10, HEIGHT/1.75))

        mousePos = pygame.mouse.get_pos()

        if settings.EGG:
            if self.playagainRect.collidepoint(mousePos):
                self.playagain = gameFont5x5small.render("Play Again", False, LIGHTLIGHTGREY)
            else:
                self.playagain = gameFont5x5small.render("Play Again", False, WHITE)
            
            if self.returntomenuRect.collidepoint(mousePos):
                self.returntomenu = gameFont5x5small.render("Return to Menu", False, LIGHTLIGHTGREY)
            else:
                self.returntomenu = gameFont5x5small.render("Return to Menu", False, WHITE)
        else:
            if self.playagainRect.collidepoint(mousePos):
                self.playagain = gameFont5x5small.render("Play Again", False, LIGHTLIGHTGREY)
            else:
                self.playagain = gameFont5x5small.render("Play Again", False, LIGHTGREY)
            
            if self.returntomenuRect.collidepoint(mousePos):
                self.returntomenu = gameFont5x5small.render("Return to Menu", False, LIGHTLIGHTGREY)
            else:
                self.returntomenu = gameFont5x5small.render("Return to Menu", False, LIGHTGREY)

        if self.coverAlpha < 215:
            self.coverAlpha += 1
            self.cover.set_alpha(self.coverAlpha)
            self.gameover.set_alpha(self.coverAlpha*(255/215 - 0.01))
            self.playagain.set_alpha(self.coverAlpha*(255/215 - 0.01))
            self.returntomenu.set_alpha(self.coverAlpha*(255/215 - 0.01))
        else:
            self.cover.set_alpha(215)
            self.gameover.set_alpha(215*(255/215 - 0.01))

    def run(self):
        self.playing = True
        self.gameState = "playing"
        while self.playing:
            self.tickspeed = self.clock.tick(FPS) / 1000.0
            self.elements.update()
            self.ballElements.update()
            self.draw()

            if self.score[0] == 5 or self.score[1] == 5:
                self.endSequence()
            
            self.counter += 1

            if self.gamemode == "bot 1v1":
                if self.counter%self.leftUpdateTime == 0:
                    if self.ball.y >= self.player1.y + self.player1.height/2 - self.leftTargeting and self.ball.y <= self.player1.y + self.player1.height/2 + self.leftTargeting and abs(self.ball.x - self.player1.x) < self.leftCloseTargeting:
                            self.player1.up = False
                            self.player1.down = False
                    else:
                        if self.ball.y + random.uniform(-1*self.leftRandomSpace,self.leftRandomSpace) < self.player1.y + self.player1.height/2 + random.uniform(-self.leftRandomSpace,self.leftRandomSpace):
                            self.player1.up = True
                            self.player1.down = False
                        else:
                            self.player1.up = False
                            self.player1.down = True

            if self.gamemode == "1 player" or self.gamemode == "bot 1v1":
                if self.counter%self.rightUpdateTime == 0:
                    if self.ball.y >= self.player2.y + self.player2.height/2 - self.rightTargeting and self.ball.y <= self.player2.y + self.player2.height/2 + self.rightTargeting and abs(self.ball.x - self.player2.x) < self.rightCloseTargeting:
                            self.player2.up = False
                            self.player2.down = False
                    else:
                        if self.ball.y + random.uniform(-1*self.rightRandomSpace,self.rightRandomSpace) < self.player2.y + self.player2.height/2 + random.uniform(-self.rightRandomSpace,self.rightRandomSpace):
                            self.player2.up = True
                            self.player2.down = False
                        else:
                            self.player2.up = False
                            self.player2.down = True

            if self.leftReady != True:
                if self.wkeyCheck.clicked and self.skeyCheck.clicked and self.dkeyCheck.clicked:
                    self.leftReady = True

            if self.rightReady != True:
                if self.upkeyCheck.clicked and self.downkeyCheck.clicked and self.leftkeyCheck.clicked:
                    self.rightReady = True

            if self.particles == "on":
                self.particleSpawner.update()

            if self.leftReady and self.rightReady:
                
                if self.coverAlpha == 0:
                    self.gameCountdown -= self.tickspeed
    
                if self.gameCountdown >= -4:
                    if math.ceil(self.gameCountdown) == 4:
                        self.hidekeybinds()
                    if math.ceil(self.gameCountdown) == 3:
                        self.drawCountdown(3)
                    elif math.ceil(self.gameCountdown) == 2:
                        self.drawCountdown(2) 
                    elif math.ceil(self.gameCountdown) == 1:
                        self.drawCountdown(1)
                    elif math.ceil(self.gameCountdown) == 0 and self.gameState == "playing":
                        self.drawCountdown("GO!")
                        self.ball.startGame()
                        self.fireball.startGame()
                        self.gameState = "active"
                    elif math.ceil(self.gameCountdown) == -1:
                        self.drawCountdown("")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if self.playagainRect.collidepoint(mousePos):
                        self.score[0] = 0 
                        self.score[1] = 0
                        self.drawScores()

                        if self.gamemode == "bot 1v1":
                            self.leftUpdateTime = random.randint(2,12)
                            self.leftRandomSpace = random.randint(0,10)
                            self.leftTargeting = random.randint(0,20)
                            self.leftCloseTargeting = random.randint(50,150)

                        if self.gamemode == "1 player" or self.gamemode == "bot 1v1":
                            self.rightUpdateTime = random.randint(2,12)
                            self.rightRandomSpace = random.randint(0,10)
                            self.rightTargeting = random.randint(20,50)
                            self.rightCloseTargeting = random.randint(50,150)

                        self.cover.set_alpha(0)
                        self.gameover.set_alpha(0)
                        self.playagain.set_alpha(0)
                        self.returntomenu.set_alpha(0)
                        self.coverAlpha = 0
                    if self.returntomenuRect.collidepoint(mousePos):
                        backToMenu()
    
    def quit(self):
        pygame.quit()
        sys.exit()