##
##  Untitled Pong Game
##  August 2022
##  Alex Starosta
##

import math
import pygame
import sys
import settings
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
            self.leftTargeting = random.randint(20,50)
            self.leftCloseTargeting = random.randint(50,150)
            self.leftPanicDistance = random.randint(100,250)
        else:
            self.leftReady = False
        self.gameCountdown = 9
        self.score = [0,0]
        self.counter = 0
        self.lcountertime = 0
        self.rcountertime = 0
        self.firecounter = 0
        self.firechange = 0
        self.fireSizeToggle = True
        self.fireballActive = False
        self.randomSide = False
        self.arrowInit = False
        self.lastTimeCheck = 0
        self.initialSide = random.randint(0,1)
        self.leftPowerup = 0
        self.rightPowerup = 0
        self.leftPowerupAllowed = False
        self.rightPowerupAllowed = False
        self.coverAlpha = 0
        self.randomfactor = random.uniform(-20,20)
        self.counter1 = 0
        self.counter2 = 0
        self.autocounter = 400
        self.hideStats = False

        if gamemode == "bot 1v1":
            self.statTableleft = [
                [
                    "Reaction",
                    self.leftUpdateTime - 2,
                    10
                ],
                [
                    "Area Scan",
                    self.leftRandomSpace,
                    10
                ],
                [
                    "Targeting",
                    self.leftTargeting - 20,
                    30
                ],
                [
                    "Side Targeting",
                    self.leftCloseTargeting - 50,
                    100
                ],
                [
                    "Calmness", 
                    self.leftPanicDistance - 100,
                    150
                ],
            ]

        if gamemode == "1 player" or gamemode == "bot 1v1":
            self.rightReady = True
            self.rightUpdateTime = random.randint(2,12)
            self.rightRandomSpace = random.randint(0,10)
            self.rightTargeting = random.randint(20,50)
            self.rightCloseTargeting = random.randint(50,150)
            self.rightPanicDistance = random.randint(100,250)
        else:
            self.rightReady = False

        if gamemode == "bot 1v1":
            self.statTableright = [
                [
                    "Reaction",
                    self.rightUpdateTime - 2,
                    10
                ],
                [
                    "Area Scan",
                    self.rightRandomSpace,
                    10
                ],
                [
                    "Targeting",
                    self.rightTargeting - 20,
                    50
                ],
                [
                    "Side Targeting",
                    self.rightCloseTargeting - 50,
                    100
                ],
                [
                    "Calmness", 
                    self.rightPanicDistance - 100,
                    150
                ],
            ]

        if gamemode == "bot 1v1":
            self.leftwins = 0
            self.rightwins = 0

    def setup(self):
        import settings
        self.elements = pygame.sprite.Group()
        self.ballElements = pygame.sprite.Group()

        if self.particles == "on":
            self.particleSpawner = ParticleSpawner()

        self.player1 = Player(self, WIDTH/50, HEIGHT/2 - HEIGHT/12, WIDTH/50, HEIGHT/6, 1, self.gamemode)
        self.player2 = Player(self, WIDTH - 2*WIDTH/50 + 1, HEIGHT/2 - HEIGHT/12, WIDTH/50, HEIGHT/6, 2, self.gamemode)

        self.fireball = Ball(self, WIDTH/2 - ((WIDTH/50)/2), HEIGHT/2, 1*settings.BALL_SPEED, 0, 0, 0, FIREORANGE, "fireball")

        self.ball = Ball(self, WIDTH/2 - ((WIDTH/50)/2), HEIGHT/2, -1*settings.BALL_SPEED, 0, WIDTH/50, WIDTH/50, LIGHTGREY, "ball")

        if not self.leftReady:
            self.wkeyCheck = KeybindChecker(self, "w", WIDTH/4 - 50, HEIGHT/3 - 170 + 50, 100, 100, DARKBLUE)
            self.skeyCheck = KeybindChecker(self, "s", WIDTH/4 - 50, HEIGHT/3 - 60 + 50, 100, 100, DARKBLUE)
            self.dkeyCheck = KeybindChecker(self, "d", WIDTH/4 + 60, HEIGHT/3 - 120 + 50, 100, 100, DARKBLUE)

            self.wsd1nonscaled = pygame.image.load("assets/wsd1.png")
            self.wsd1 = pygame.transform.scale(self.wsd1nonscaled, (220,220))
            self.wsd1Rect = self.wsd1.get_rect(center = (WIDTH/2 - 200, HEIGHT/4 + 50))

        if not self.rightReady:
            self.upkeyCheck = KeybindChecker(self, "up", WIDTH/2 + WIDTH/4 - 50, HEIGHT/3 - 170 + 50, 100, 100, DARKRED)
            self.downkeyCheck = KeybindChecker(self, "down", WIDTH/2 + WIDTH/4 - 50, HEIGHT/3 - 60 + 50, 100, 100, DARKRED)
            self.leftkeyCheck = KeybindChecker(self, "left", WIDTH/2 + WIDTH/4 - 160, HEIGHT/3 - 120 + 50, 100, 100, DARKRED)

            self.udl1nonscaled = pygame.image.load("assets/updownleft1.png")
            self.udl1 = pygame.transform.scale(self.udl1nonscaled, (220,220))
            self.udl1Rect = self.udl1.get_rect(center = (WIDTH/2 + 200,HEIGHT/4 + 50))

        gameFont5x5 = pygame.font.Font("assets/bit5x5.ttf", 172)
        self.startingText = gameFont5x5.render("", False, LIGHTGREY)
        self.startingTextRect = self.startingText.get_rect(center = (WIDTH/1.92 - ((WIDTH/50)/2), HEIGHT/4))

        gameFont5x3 = pygame.font.Font("assets/bit5x3.ttf", 112)
        gameFont5x3small = pygame.font.Font("assets/bit5x5.ttf", 26)

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

        if self.gamemode == "bot 1v1":
            self.hiscoreLeft = gameFont5x3small.render(f"{self.leftwins}", False, LIGHTGREY)
            self.hiscoreLeftRect = self.hiscoreLeft.get_rect(midleft = (56, 120))

            self.hiscoreRight = gameFont5x3small.render(f"{self.rightwins}", False, LIGHTGREY)
            self.hiscoreRightRect = self.hiscoreRight.get_rect(midright = (WIDTH-52, 120))

            self.crownnonscaled = pygame.image.load("assets/crown.png")
            self.crown = pygame.transform.scale(self.crownnonscaled, (80,100))
            self.crownRect = self.crown.get_rect()
            self.crown.set_alpha(0)

            self.headingTab = []
            self.headingRectTab = []
            self.rectTab = []
            for stat in self.statTableleft:
                i = self.counter1

                heading = gameFont5x3small.render(f"{stat[0]}", False, LIGHTLIGHTGREY)
                headingRect = heading.get_rect(midleft = (30, HEIGHT - 182 + (i*35)))

                self.headingTab.insert(1,heading)
                self.headingRectTab.insert(1,headingRect)

                self.counter1 += 1

            for stat in self.statTableright:
                i = self.counter2

                heading = gameFont5x3small.render(f"{stat[0]}", False, LIGHTLIGHTGREY)
                headingRect = heading.get_rect(midright = (WIDTH - 27, HEIGHT - 182 + (i*35)))

                self.headingTab.insert(1,heading)
                self.headingRectTab.insert(1,headingRect)

                self.counter2 += 1

            self.counter1 = 0 
            self.counter2 = 0

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

        if self.gamemode == "bot 1v1":
            gameFont5x3small = pygame.font.Font("assets/bit5x3.ttf", 22)
            self.screen.blit(self.crown, self.crownRect)
            if self.leftwins != 0:
                self.hiscoreLeft = gameFont5x3small.render(f"{self.leftwins}", False, LIGHTGREY)
                self.screen.blit(self.hiscoreLeft, self.hiscoreLeftRect)
            if self.rightwins != 0:
                self.hiscoreRight = gameFont5x3small.render(f"{self.rightwins}", False, LIGHTGREY)
                self.hiscoreRightRect = self.hiscoreRight.get_rect(midright = (WIDTH-52, 120))
                self.screen.blit(self.hiscoreRight, self.hiscoreRightRect)
            
            if not self.hideStats:

                for stat in self.statTableleft:
                    i = self.counter1
                    if stat[0] == "Reaction":
                        pygame.draw.rect(self.screen, DARKBLUE, (19, HEIGHT - 195 + (i*35), 150*((10-stat[1])/stat[2]), 25))
                    else:
                        pygame.draw.rect(self.screen, DARKBLUE, (19, HEIGHT - 195 + (i*35), 150*(stat[1]/stat[2]), 25))
                    pygame.draw.rect(self.screen, LIGHTGREY, (19, HEIGHT - 197 + (i*35), 5, 29))
                    self.counter1 += 1

                for stat in self.statTableright:
                    i = self.counter2
                    if stat[0] == "Reaction":
                        pygame.draw.rect(self.screen, DARKRED, (WIDTH - 20 - 150*((10-stat[1])/stat[2]), HEIGHT - 195 + (i*35), 150*((10-stat[1])/stat[2]), 25))
                    else:
                        pygame.draw.rect(self.screen, DARKRED, (WIDTH - 20 - 150*(stat[1]/stat[2]), HEIGHT - 195 + (i*35), 150*(stat[1]/stat[2]), 25))
                    pygame.draw.rect(self.screen, LIGHTGREY, (WIDTH - 23, HEIGHT - 197 + (i*35), 5, 29))
                    self.counter2 += 1

                self.counter1 = 0 
                self.counter2 = 0

                for h in range(len(self.headingTab)):
                    self.screen.blit(self.headingTab[h], self.headingRectTab[h])

        if self.coverAlpha != 0:
            self.screen.blit(self.cover, self.coverRect)
            self.screen.blit(self.gameover, self.gameoverRect)
            self.screen.blit(self.playagain, self.playagainRect)
            self.screen.blit(self.returntomenu, self.returntomenuRect)
            if self.gamemode == "bot 1v1":
                self.screen.blit(self.autobots, self.autobotsRect)
                if self.autocounter != 400:
                    pygame.draw.rect(self.screen, LIGHTGREY, (WIDTH/2 - 180 - 120*(self.autocounter/400)/2, HEIGHT/1.75 + 40, 120 *(self.autocounter/400), 15))

        if self.randomSide == False and self.arrowInit:
            self.screen.blit(self.arrow, self.arrowRect)

        if self.coverAlpha == 0:
            import settings
            for i in range(settings.POWERUP_BOUNCE_AMOUNT):
                pygame.draw.rect(self.screen, LIGHTGREY, (140 + (i*40), 23, 35, 35), 5)
                pygame.draw.rect(self.screen, LIGHTGREY, (WIDTH - (140 + (i*40) + 35), 23, 35, 35), 5)

            if self.player1.hits <= settings.POWERUP_BOUNCE_AMOUNT:
                for i in range(self.player1.hits):
                    pygame.draw.rect(self.screen, LIGHTGREY, (140 + (i*40), 23, 35, 35))
            else:
                for i in range(settings.POWERUP_BOUNCE_AMOUNT):
                    pygame.draw.rect(self.screen, LIGHTGREY, (140 + (i*40), 23, 35, 35))

            if self.player2.hits <= settings.POWERUP_BOUNCE_AMOUNT:
                for i in range(self.player2.hits):
                    pygame.draw.rect(self.screen, LIGHTGREY, (WIDTH - (140 + (i*40) + 35), 23, 35, 35))
            else:
                for i in range(settings.POWERUP_BOUNCE_AMOUNT):
                    pygame.draw.rect(self.screen, LIGHTGREY, (WIDTH - (140 + (i*40) + 35), 23, 35, 35))

            if self.leftPowerup != 0:
                pygame.draw.rect(self.screen, BLUE, (140, 66 + 2.5, 120*(self.leftPowerup/(settings.POWERUP_TIME*100)), 20))
                pygame.draw.rect(self.screen, LIGHTGREY, (140, 66, 5, 25))

            if self.rightPowerup != 0:
                pygame.draw.rect(self.screen, RED, (WIDTH - 140 - 120*(self.rightPowerup/(settings.POWERUP_TIME*100)), 66 + 2.5, 120*(self.rightPowerup/(settings.POWERUP_TIME*100)), 20))
                pygame.draw.rect(self.screen, LIGHTGREY, (WIDTH - 140 - 5, 66, 5, 25))

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

    def restartPlayAgain(self):

        self.autocounter = 400

        if self.gamemode == "bot 1v1":
            import settings
            self.crown.set_alpha(255)
            if self.score[0] < self.score[1]:
                self.leftUpdateTime = random.randint(2,12)
                self.leftRandomSpace = random.randint(0,10)
                self.leftTargeting = random.randint(20,50)
                self.leftCloseTargeting = random.randint(50,150)
                self.leftPanicDistance = random.randint(100,250)
                self.rightwins += 1
                self.leftwins = 0
                self.crownRect = self.crown.get_rect(center = (WIDTH - 37,120))

                if self.rightwins > settings.BOT_HISCORE:
                    settings.BOT_HISCORE = self.rightwins
                    
            else:
                self.rightUpdateTime = random.randint(2,12)
                self.rightRandomSpace = random.randint(0,10)
                self.rightTargeting = random.randint(20,50)
                self.rightCloseTargeting = random.randint(50,150)
                self.rightPanicDistance = random.randint(100,250)
                self.leftwins += 1
                self.rightwins = 0
                self.crownRect = self.crown.get_rect(center = (33,120))

                if self.leftwins > settings.BOT_HISCORE:
                    settings.BOT_HISCORE = self.leftwins

            self.statTableleft = [
                [
                    "Reaction",
                    self.leftUpdateTime - 2,
                    10
                ],
                [
                    "Area Scan",
                    self.leftRandomSpace,
                    10
                ],
                [
                    "Targeting",
                    self.leftTargeting - 20,
                    30
                ],
                [
                    "Side Targeting",
                    self.leftCloseTargeting - 50,
                    100
                ],
                [
                    "Calmness", 
                    self.leftPanicDistance - 100,
                    150
                ],
            ]

            self.statTableright = [
                [
                    "Reaction",
                    self.rightUpdateTime - 2,
                    10
                ],
                [
                    "Area Scan",
                    self.rightRandomSpace,
                    10
                ],
                [
                    "Targeting",
                    self.rightTargeting - 20,
                    50
                ],
                [
                    "Side Targeting",
                    self.rightCloseTargeting - 50,
                    100
                ],
                [
                    "Calmness", 
                    self.rightPanicDistance - 100,
                    150
                ],
            ]

        self.score[0] = 0 
        self.score[1] = 0
        self.drawScores()
        self.player1.hits = 0
        self.player2.hits = 0
        self.leftPowerup = 0
        self.rightPowerup = 0
        self.leftPowerupAllowed = False
        self.rightPowerupAllowed = False

        if self.gamemode == "1 player":
            self.rightUpdateTime = random.randint(2,12)
            self.rightRandomSpace = random.randint(0,10)
            self.rightTargeting = random.randint(20,50)
            self.rightCloseTargeting = random.randint(50,150)

        self.cover.set_alpha(0)
        self.gameover.set_alpha(0)
        self.playagain.set_alpha(0)
        self.returntomenu.set_alpha(0)
        self.autobots.set_alpha(0)
        self.coverAlpha = 0
        self.gameCountdown = 9
        self.initialSide = random.randint(0,1)
        self.randomSide = False
        self.arrowInit = False

    def endSequence(self):
        
        if self.score[0] == 0 and self.score[1] == 0:
            return
        
        import settings
        if settings.AUTOPLAY_BOTS:
            if self.autocounter > 0:
                self.autocounter -= 1
            else:
                self.coverAlpha = 0
                self.restartPlayAgain()
                return

        gameFont5x5 = pygame.font.Font("assets/bit5x5.ttf", 100)
        gameFont5x5small = pygame.font.Font("assets/bit5x5.ttf", 30)
        gameFont5x5smallsmall = pygame.font.Font("assets/bit5x5.ttf", 18)

        self.cover = pygame.Surface([WIDTH, HEIGHT])
        self.cover.fill(DARKGREY)
        self.coverRect = self.cover.get_rect(center = (WIDTH/2, HEIGHT/2))
        
        if settings.EGG:
            self.gameover = gameFont5x5.render("Game Over", False, WHITE)
            self.playagain = gameFont5x5small.render("Play Again", False, WHITE)
            self.returntomenu = gameFont5x5small.render("Return to Menu", False, WHITE)
            if settings.AUTOPLAY_BOTS:
                self.autobots = gameFont5x5small.render("Autoplay Bots", False, GREEN)
            else:
                self.autobots = gameFont5x5small.render("Autoplay Bots", False, RED)
        else:
            self.gameover = gameFont5x5.render("Game Over", False, LIGHTGREY)
            self.playagain = gameFont5x5small.render("Play Again", False, LIGHTGREY)
            self.returntomenu = gameFont5x5small.render("Return to Menu", False, LIGHTGREY)
            if settings.AUTOPLAY_BOTS:
                self.autobots = gameFont5x5smallsmall.render("Autoplay Bots", False, DARKGREEN)
            else:
                self.autobots = gameFont5x5smallsmall.render("Autoplay Bots", False, DARKRED)

        self.gameoverRect = self.gameover.get_rect(center = (WIDTH/2, HEIGHT/2.5))
        self.playagainRect = self.playagain.get_rect(midright = (WIDTH/2 - 70, HEIGHT/1.75))
        self.autobotsRect = self.autobots.get_rect(midright = (WIDTH/2 - 93, HEIGHT/1.75 + 25))
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
            
            if settings.AUTOPLAY_BOTS:
                if self.autobotsRect.collidepoint(mousePos):
                    self.autobots = gameFont5x5smallsmall.render("Autoplay Bots", False, GREEN)
                else:
                    self.autobots = gameFont5x5smallsmall.render("Autoplay Bots", False, DARKGREEN)
            else:
                if self.autobotsRect.collidepoint(mousePos):
                    self.autobots = gameFont5x5smallsmall.render("Autoplay Bots", False, RED)
                else:
                    self.autobots = gameFont5x5smallsmall.render("Autoplay Bots", False, DARKRED)
        else:
            if self.playagainRect.collidepoint(mousePos):
                self.playagain = gameFont5x5small.render("Play Again", False, LIGHTLIGHTGREY)
            else:
                self.playagain = gameFont5x5small.render("Play Again", False, LIGHTGREY)
            
            if self.returntomenuRect.collidepoint(mousePos):
                self.returntomenu = gameFont5x5small.render("Return to Menu", False, LIGHTLIGHTGREY)
            else:
                self.returntomenu = gameFont5x5small.render("Return to Menu", False, LIGHTGREY)
            
            if settings.AUTOPLAY_BOTS:
                if self.autobotsRect.collidepoint(mousePos):
                    self.autobots = gameFont5x5smallsmall.render("Autoplay Bots", False, GREEN)
                else:
                    self.autobots = gameFont5x5smallsmall.render("Autoplay Bots", False, DARKGREEN)
            else:
                if self.autobotsRect.collidepoint(mousePos):
                    self.autobots = gameFont5x5smallsmall.render("Autoplay Bots", False, RED)
                else:
                    self.autobots = gameFont5x5smallsmall.render("Autoplay Bots", False, DARKRED)

        if self.coverAlpha < 215:
            self.coverAlpha += 1
            self.cover.set_alpha(self.coverAlpha)
            self.gameover.set_alpha(self.coverAlpha*(255/215 - 0.01))
            self.playagain.set_alpha(self.coverAlpha*(255/215 - 0.01))
            self.returntomenu.set_alpha(self.coverAlpha*(255/215 - 0.01))
            self.autobots.set_alpha(self.coverAlpha*(255/215 - 0.01))
        else:
            self.cover.set_alpha(215)
            self.gameover.set_alpha(215*(255/215 - 0.01))

    def randomStart(self, change):
        gameFont5x5small = pygame.font.Font("assets/bit5x5.ttf", 30)
        if self.score[0] == 0 and self.score[1] == 0:
            self.arrowInit = True

            if change:
                if self.initialSide == 1:
                    self.initialSide = 0
                else:
                    self.initialSide = 1

            if self.initialSide == 1:
                self.arrow = gameFont5x5small.render("-}", False, LIGHTGREY)
            else:
                self.arrow = gameFont5x5small.render("{-", False, LIGHTGREY)
            self.arrowRect = self.arrow.get_rect(center = (WIDTH/2, HEIGHT/2.5))
        else:
            if self.ball.lastWinner == "right":
                self.arrow = gameFont5x5small.render("{-", False, LIGHTGREY)
            else:
                self.arrow = gameFont5x5small.render("-}", False, LIGHTGREY)
            self.arrowRect = self.arrow.get_rect(center = (WIDTH/2, HEIGHT/2.5))     
    
    def run(self):
        self.playing = True
        self.gameState = "playing"
        while self.playing:
            import settings
            self.tickspeed = self.clock.tick(settings.FPS) / 1000.0
            self.elements.update()
            self.ballElements.update()
            self.draw()

            if self.score[0] == settings.WIN_SCORE or self.score[1] == settings.WIN_SCORE:
                self.endSequence()

            self.counter += 1

            if self.gamemode == "bot 1v1":
                import settings
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
                    if abs(self.ball.y - self.player1.y + self.player1.height/2) > self.leftPanicDistance and abs(self.ball.x - self.player1.x) < self.leftCloseTargeting*2 and self.leftPowerupAllowed and self.ball.xVel < 0:
                        self.leftPowerupAllowed = False
                        self.player1.hits = 0
                        self.leftPowerup = settings.POWERUP_TIME * 100

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
                    if abs(self.ball.y - self.player2.y + self.player2.height/2) > self.rightPanicDistance and abs(self.ball.x - self.player2.x) < self.rightCloseTargeting*2 and self.rightPowerupAllowed and self.ball.xVel > 0:
                        self.rightPowerupAllowed = False
                        self.player2.hits = 0
                        self.rightPowerup = settings.POWERUP_TIME * 100

            if self.leftReady != True:
                if self.wkeyCheck.clicked and self.skeyCheck.clicked and self.dkeyCheck.clicked:
                    self.leftReady = True

            if self.rightReady != True:
                if self.upkeyCheck.clicked and self.downkeyCheck.clicked and self.leftkeyCheck.clicked:
                    self.rightReady = True

            if self.particles == "on":
                self.particleSpawner.update()

            import settings
            if self.player1.hits == settings.POWERUP_BOUNCE_AMOUNT:
                self.leftPowerupAllowed = True

            if self.player2.hits == settings.POWERUP_BOUNCE_AMOUNT:
                self.rightPowerupAllowed = True

            if self.leftPowerup != 0:
                self.leftPowerup -= 1
                self.player1.powerup = True
            else:
                self.player1.powerup = False

            if self.rightPowerup != 0:
                self.rightPowerup -= 1
                self.player2.powerup = True
            else:
                self.player2.powerup = False

            if self.leftReady and self.rightReady:
                
                if math.ceil(self.gameCountdown) <= 8:
                    self.hidekeybinds()

                if self.coverAlpha == 0:
                    self.gameCountdown -= self.tickspeed

                def sideSequence():

                    if round(self.gameCountdown,1) == self.lastTimeCheck:
                        return

                    for i in range(11):
                        if round(self.gameCountdown,1) == (round (7 - (-math.sqrt(-i+10)+3.162),1)):
                            self.randomStart(True)
                            return

                    self.randomStart(False)
                
                if self.randomSide == False and math.ceil(self.gameCountdown) <= 7 and math.ceil(self.gameCountdown) > 3.5:
                    if self.score[0] == 0 and self.score[1] == 0:
                        sideSequence()
                        self.lastTimeCheck = round(self.gameCountdown,1)

                if self.gameCountdown >= -4:
                    if math.ceil(self.gameCountdown) == 3:
                        self.drawCountdown(3)
                        if self.score[0] == 0 and self.score[1] == 0:
                            if self.initialSide == 0:
                                self.ball.lastWinner = "right"
                            else:
                                self.ball.lastWinner = "left"
                        else:
                            self.randomSide = False
                            self.randomStart(False)
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
                        self.arrowInit = False
                        self.randomSide = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                    if event.key == pygame.K_TAB:
                        self.hideStats = not self.hideStats
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    import settings
                    if self.score[0] == settings.WIN_SCORE or self.score[1] == settings.WIN_SCORE:
                        if self.playagainRect.collidepoint(mousePos):
                            if self.score[0] > self.score[1] and self.gamemode == "1 player":
                                settings.WINS += 1
                            self.restartPlayAgain()

                        if self.returntomenuRect.collidepoint(mousePos):
                            if self.score[0] > self.score[1] and self.gamemode == "1 player":
                                settings.WINS += 1
                            backToMenu()

                        if self.autobotsRect.collidepoint(mousePos):
                            import settings
                            settings.AUTOPLAY_BOTS = not settings.AUTOPLAY_BOTS
    
    def quit(self):
        pygame.quit()
        sys.exit()