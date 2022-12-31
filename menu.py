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

def enterCommand(command):
    c = command
    cs = c.split(" ")

    import settings
    import audio

    itemlist = ["fps", "paddle_speed", "ball_speed", "win_require", "p_time", "p_increase", "p_bounce"]

    statlist = ["wins", "hits", "fireballs", "bot_hiscore"]

    if c == "help":
        return "available commands: change, view, itemlist, statlist, reset_items, reset_stats, controls"
    if c == "change" or cs[0] == "change":
        if len(cs) > 2:
            if cs[1] in itemlist:
                if cs[2].isnumeric():
                    if int(cs[2]) <= 0:
                        return "please enter a value greater than zero for item " + f"{cs[1]}"
                    i = itemlist.index(cs[1])
                    if i == 0:
                        settings.FPS = int(cs[2])
                    elif i == 1:
                        settings.PADDLE_SPEED = int(cs[2])
                    elif i == 2:
                        settings.BALL_SPEED = int(cs[2])
                    elif i == 3:
                        settings.WIN_SCORE = int(cs[2])
                    elif i == 4:
                        settings.POWERUP_TIME = int(cs[2])
                    elif i == 5:
                        settings.POWERUP_INCREASE = int(cs[2])
                    elif i == 6:
                        settings.POWERUP_BOUNCE_AMOUNT = int(cs[2])
                    if settings.SFX == "on":
                        audio.consolegoodSfx.play()
                    return f"{itemlist[i]}" + " was changed to " + f"{cs[2]}"
                if settings.SFX == "on":
                    audio.consolebadSfx.play()
                return "please enter a numeric value for item " + f"{cs[1]}"
            if settings.SFX == "on":
                audio.consolebadSfx.play()
            return "item " + f"{cs[1]}" + " not found in itemlist"
        return "enter 'change <item> <value>' to change an items value"
    if c == "view" or cs[0] == "view":
        if len(cs) > 1:
            if cs[1] in itemlist:
                i = itemlist.index(cs[1])
                if i == 0:
                    return "the current fps is " + f"{settings.FPS}"
                elif i == 1:
                    return "the current paddle speed is " + f"{settings.PADDLE_SPEED}" + " speed units"
                elif i == 2:
                    return "the current ball speed is " + f"{settings.BALL_SPEED}"
                elif i == 3:
                    return "the score needed to win is " + f"{settings.WIN_SCORE}"
                elif i == 4:
                    return "the current powerup time is " + f"{settings.POWERUP_TIME}" + " game units"
                elif i == 5:
                    return "the current powerup increase is " + f"{settings.POWERUP_INCREASE}" + " speed units"
                elif i == 6:
                    return "the amount of bounces need to get a powerup is " + f"{settings.POWERUP_BOUNCE_AMOUNT}" + " bounces"
            elif cs[1] in statlist:
                i = statlist.index(cs[1])
                if i == 0:
                    return "total wins: " + f"{settings.WINS}"
                elif i == 1:
                    return "total hits: " + f"{settings.HITS}"
                elif i == 2:
                    return "total fireballs: " + f"{settings.FIREBALLS}"
                elif i == 3:
                    return "highest bot score: " + f"{settings.BOT_HISCORE}"
            if settings.SFX == "on":
                audio.consolebadSfx.play()
            return "item " + f"{cs[1]}" + " not found in itemlist or statlist"
        return "enter 'view <item>' to view an item or stat value"
    if c == "itemlist" or cs[0] == "itemlist":
        return "avaiable items: fps, paddle_speed, ball_speed, win_require, p_time, p_increase, p_bounce"
    if c == "statlist" or cs[0] == "statlist":
        return "avaiable stats: wins, hits, fireballs, bot_hiscore"
    if c == "reset_items" or cs[0] == "reset_items":
        settings.FPS = 60
        settings.PADDLE_SPEED = 8
        settings.BALL_SPEED = 7
        settings.WIN_SCORE = 4
        settings.POWERUP_INCREASE = 7
        settings.POWERUP_TIME = 3
        settings.POWERUP_BOUNCE_AMOUNT = 3
        if settings.SFX == "on":
            audio.consolegoodSfx.play()
        return "items successfully reset"
    if c == "reset_stats" or cs[0] == "reset_stats":
        settings.WINS = 0
        settings.HITS = 0
        settings.FIREBALLS = 0
        settings.BOT_HISCORE = 0
        if settings.SFX == "on":
            audio.consolegoodSfx.play()
        return "stats successfully reset"
    if c == "hi":
        return "hi :)"
    if c == "exit":
        if settings.SFX == "on":
            audio.buttonSfx.play()
        return "exiting..."
    if c == "controls":
        return "controls"
    if settings.SFX == "on":
        audio.consolebadSfx.play()
    return "unknown command '" + f"{cs[0]}" + "', type 'help' for more info"

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

        self.consoleActive = False
        self.consoleResponse = []
        self.userInput = ""

    def setup(self):
        self.elements = pygame.sprite.Group()

        self.particleSpawner = ParticleSpawner()

        gameFont5x5small = pygame.font.Font("assets/bit5x5.ttf", 32)
        terminalFont = pygame.font.Font("assets/terminalFont.ttf", 16)
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

        self.userInputRender = terminalFont.render(f"{self.userInput}", False, GREEN)
        self.consoleStart = terminalFont.render("C:/UntitledPongGame/>", False, GREEN)

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

        if self.consoleActive:
            console = pygame.Surface((WIDTH,HEIGHT/4))
            console.set_alpha(128)
            console.fill((0,0,0))
            self.screen.blit(console, (0,0))

            self.userInputRenderRect = self.userInputRender.get_rect(bottomleft = (217, HEIGHT/4 - 5))
            self.screen.blit(self.userInputRender, self.userInputRenderRect)

            self.consoleStartRect = self.consoleStart.get_rect(bottomleft = (5, HEIGHT/4 - 5))
            self.screen.blit(self.consoleStart, self.consoleStartRect)

            if len(self.consoleResponse) != 0:
                for i in range(len(self.consoleResponse)):
                    terminalFont = pygame.font.Font("assets/terminalFont.ttf", 16)

                    self.text = terminalFont.render(f"{self.consoleResponse[i]}", False, GREEN)
                    self.textRect = self.userInputRender.get_rect(bottomleft = (5, HEIGHT/4 - 50 - (i*25)))
                    self.screen.blit(self.text, self.textRect)

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
            import settings
            self.tickspeed = self.clock.tick(settings.FPS) / 1000
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
                    if event.key == pygame.K_BACKQUOTE or event.key == pygame.K_RALT:
                        import audio
                        import settings
                        if settings.SFX == "on":
                            audio.buttonSfx.play()
                        self.consoleActive = not self.consoleActive
                if self.consoleActive:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.userInput = self.userInput[:-1]
                            terminalFont = pygame.font.Font("assets/terminalFont.ttf", 16)
                            self.userInputRender = terminalFont.render(f"{self.userInput}", False, GREEN)
                        elif event.key == pygame.K_RETURN and self.userInput != "":
                            if enterCommand(self.userInput) == "controls":
                                self.consoleResponse.insert(0,"movement controls : W/up arrow = up, S/down arrow = down, D/left arrow = powerup")
                                self.consoleResponse.insert(0,"bot 1v1 controls  : tab = hide bot stats, L = leave match")
                                self.userInput = ""
                                terminalFont = pygame.font.Font("assets/terminalFont.ttf", 16)
                                self.userInputRender = terminalFont.render(f"{self.userInput}", False, GREEN)
                            else:
                                if enterCommand(self.userInput) == "exiting...":
                                    self.consoleActive = not self.consoleActive
                                self.consoleResponse.insert(0,enterCommand(self.userInput))
                                self.userInput = ""
                                terminalFont = pygame.font.Font("assets/terminalFont.ttf", 16)
                                self.userInputRender = terminalFont.render(f"{self.userInput}", False, GREEN)
                        else:
                            if event.key != pygame.K_BACKQUOTE and event.key != pygame.K_RETURN:
                                self.userInput += event.unicode
                                terminalFont = pygame.font.Font("assets/terminalFont.ttf", 16)
                                self.userInputRender = terminalFont.render(f"{self.userInput}", False, GREEN)
                if self.counter > 3 and not self.consoleActive:
                    import audio
                    import settings
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.playButtonRect.collidepoint(mousePos):
                            if settings.SFX == "on":
                                audio.buttonSfx.play()
                            updateValues(self.sfxSetting, self.particleSetting, self.gamemode)
                            startGame(self.gamemode, self.sfxSetting, self.particleSetting)
                        elif self.optionsButtonRect.collidepoint(mousePos):
                            if settings.SFX == "on":
                                audio.buttonSfx.play()
                            if self.optionsOpen:
                                self.setupOptions("close")
                            else:
                                self.setupCredits("close")
                                self.setupOptions("open")
                        elif self.creditsButtonRect.collidepoint(mousePos):
                            if settings.SFX == "on":
                                audio.buttonSfx.play()
                            if self.creditsOpen:
                                self.setupCredits("close")
                            else:
                                self.setupOptions("close")
                                self.setupCredits("open")

                        if self.textoRect.collidepoint(mousePos):
                            if settings.SFX == "on":
                                audio.ostrikeSfx.play()
                            self.oclick += 1
                            self.particleSpawner.spawnParticles(LIGHTGREY, mousePos[0], mousePos[1], "fire")
                            if self.oclick > 2:
                                self.ofall = True
                            else:
                                self.textoRect.y += 5

                        if self.optionsOpen:
                            if self.sfxButtonActionRect.collidepoint(mousePos):
                                if self.sfxSetting == "on":
                                    import settings
                                    settings.SFX = "off"
                                    self.sfxSetting = "off"
                                else:
                                    audio.sfxonSfx.play()
                                    settings.SFX = "on"
                                    self.sfxSetting = "on"
                            self.reRenderSettings()
                    
                            if self.partiButtonActionRect.collidepoint(mousePos):
                                if settings.SFX == "on":
                                    audio.buttonSfx.play()
                                if self.particleSetting == "on":
                                    self.particleSetting = "off"
                                else:
                                    self.particleSetting = "on"
                                    self.particleSpawner.spawnParticles(LIGHTRED, mousePos[0], mousePos[1], "corner")
                            self.reRenderSettings()

                            if self.modeButtonActionRect.collidepoint(mousePos):
                                if settings.SFX == "on":
                                    audio.buttonSfx.play()
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