import pygame as pg
from playelements import *
from utilities import *
from definitions import *
from os import path
from pathfinding import *

class PlayScreen:
    def __init__(self, parent):
        self.parent = parent
        self.currentLevel = 0
        self.startLevel(LEVELPATHS[0])
    
    def startLevel(self, levelFilePath):
        self.gameComplete = False
        self.createMapFromFile(levelFilePath)
        self.player = Player(self.startLocation[0], self.startLocation[1], TILESIZE)
        self.playerInterval = 0
        #from BensPF import Pathfinding
        #pathFinder = Pathfinding(self.map, [self.startLocation[1], self.startLocation[0]], [self.endLocation[1], self.endLocation[0]])
        #path = pathFinder.findPath()

        path = astar(self.map, (self.startLocation[1], self.startLocation[0]), (self.endLocation[1], self.endLocation[0]))

        self.computer = Computer(self.startLocation[0], self.startLocation[1], TILESIZE, path)
        self.computerInterval = 0
        self.camera = Camera(WIDTH, HEIGHT, TILESIZE, self.player, self.map)
        self.mapDisplay = MapDisplay(self.map, TILESIZE)
    
    def createMapFromFile(self, filePath):
        dir = path.dirname(__file__)
        self.map = []  # empty list to store map data
        with open(path.join(dir, 'Levels/'+filePath), 'rt') as f:
            for line in f:
                mapLine = []
                for c in line.rstrip():
                    mapLine.append(c)
                self.map.append(mapLine)  # read in map line-by-line
        
        for row, tiles in enumerate(self.map): # Need to fix this
            for col, tile in enumerate(tiles):
                if tile == '2':
                    self.startLocation = (col, row)
                if tile == '3':
                    self.endLocation = (col, row)

    
    def draw(self, screen):
        screen.fill(BLACK)
        self.camera.moveCamera(self.player)

        self.mapDisplay.draw(screen, self.camera)
        self.computer.draw(screen, self.camera)
        self.player.draw(screen, self.camera)

        if self.gameComplete:
            font = pg.font.Font(None, 100)
            if self.playerWin:
                if self.currentLevel >= len(LEVELPATHS)-1:
                    font = pg.font.Font(None, 70)
                    text = font.render("Congratulations! You beat the Game!", True, GREEN)
                else:
                    text = font.render("Press Enter to Continue", True, WHITE)
            else:
                text = font.render("BEN IS A LOSER", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(text, text_rect)
    
    def update(self):
        self.playerWin = self.player.checkWin(self.map)
        self.computerWin = self.computer.checkWin()

        if self.playerWin:
            self.gameComplete = True
        
        if self.computerWin:
            self.gameComplete = True

        if not self.gameComplete:
            self.playerInterval += 1

            if self.playerInterval % PLAYER_MOVE_RATE == 0:
                self.player.move(self.map)

            self.computerInterval += 1
            
            if self.computerInterval % COMPUTER_PLAY_RATE == 0:
                self.computerInterval = 0
                self.computer.move()
    
    def handleEvents(self, event):
        if not self.gameComplete:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.clearVel()
                    self.player.yVel = -1
                    #self.player.move(self.map, PLAYER_UP)
                if event.key == pg.K_DOWN:
                    self.player.clearVel()
                    self.player.yVel = 1
                    #self.player.move(self.map, PLAYER_DOWN)
                if event.key == pg.K_LEFT:
                    self.player.clearVel()
                    self.player.xVel = -1
                    #self.player.move(self.map, PLAYER_LEFT)
                if event.key == pg.K_RIGHT:
                    self.player.clearVel()
                    self.player.xVel = 1
                    #self.player.move(self.map, PLAYER_RIGHT)
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    if self.player.yVel == -1:
                        self.player.clearVel()
                    #self.player.move(self.map, PLAYER_UP)
                if event.key == pg.K_DOWN:
                    if self.player.yVel == 1:
                        self.player.clearVel()
                    #self.player.move(self.map, PLAYER_DOWN)
                if event.key == pg.K_LEFT:
                    if self.player.xVel == -1:
                        self.player.clearVel()
                    #self.player.move(self.map, PLAYER_LEFT)
                if event.key == pg.K_RIGHT:
                    if self.player.xVel == 1:
                        self.player.clearVel()
                    #self.player.move(self.map, PLAYER_RIGHT)
        else:
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    if self.playerWin:
                        self.currentLevel += 1
                    if self.currentLevel == len(LEVELPATHS):
                        self.parent.running = False
                        return
                    self.startLevel(LEVELPATHS[self.currentLevel])
                
        