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
        self.startLevel(LEVELPATHS[0]) # Start game at first level
    
    def startLevel(self, levelFilePath):
        self.gameComplete = False
        self.createMapFromFile(levelFilePath)

        self.player = Player(self.startLocation[0], self.startLocation[1], self.tileSize)
        self.playerInterval = 0

        path = breadthFirst(self.map, (self.startLocation[1], self.startLocation[0]), (self.endLocation[1], self.endLocation[0]))
        self.player.movesLeft = int((len(path) * 1.2)) # Player has to take a short-ish path
        self.computer = Computer(self.startLocation[0], self.startLocation[1], self.tileSize, path)
        self.computerInterval = 0

        #Used for scrolling maps
        self.camera = Camera(WIDTH, HEIGHT, self.tileSize, self.player, self.map)
        self.mapDisplay = MapDisplay(self.map, self.tileSize)
    
    def createMapFromFile(self, filePath):
        dir = path.dirname(__file__)
        self.map = []  # empty list to store map data
        with open(path.join(dir, 'Levels/'+filePath), 'rt') as f:
            params = f.__next__().split(':') # Map settings
            self.tileSize = int(params[0])
            self.computerPlayRate = int(params[1])
            self.playerMoveRate = int(params[2])
            for line in f:
                mapLine = []
                for c in line.rstrip():
                    mapLine.append(c) # read in map character by character
                self.map.append(mapLine)
        
        for row, tiles in enumerate(self.map): # Get start and end location
            for col, tile in enumerate(tiles):
                if tile == '2':
                    self.startLocation = (col, row)
                if tile == '3':
                    self.endLocation = (col, row)

    
    def draw(self, screen):
        screen.fill(BLACK)
        self.camera.moveCamera(self.player)

        # Draw order: Map < Computer < Player
        self.mapDisplay.draw(screen, self.camera)
        self.computer.draw(screen, self.camera)
        self.player.draw(screen, self.camera)

        if self.gameComplete: # Round is over, display message
            font = pg.font.Font(None, 100)
            if self.playerWin: # Player has reached the end
                if self.currentLevel >= len(LEVELPATHS)-1: # Player has finished all levels
                    font = pg.font.Font(None, 70)
                    text = font.render("Congratulations! You beat the Game!", True, GREEN)
                else:
                    text = font.render("You completed the level!", True, WHITE)
            elif self.outOfMoves: # Player has run out of moves
                text = font.render("You have run out of moves!", True, WHITE)
            else: # Computer has reached the end
                text = font.render("The computer has won!", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2)) # Center text on screen
            screen.blit(text, text_rect)
            continueText = font.render("Press Enter to Continue.", True, WHITE)
            continueText_rect = continueText.get_rect(center=(WIDTH/2, HEIGHT/2 + 100))
            screen.blit(continueText, continueText_rect)
    
    def update(self):
        self.outOfMoves = self.player.movesLeft <= 0 # Player has ran out of moves
        self.playerWin = self.player.checkWin(self.map)
        self.computerWin = self.computer.checkWin()

        if self.outOfMoves:
            self.gameComplete = True

        if self.playerWin:
            self.gameComplete = True
        
        if self.computerWin:
            self.gameComplete = True

        if not self.gameComplete:
            self.playerInterval += 1

            if self.playerInterval % self.playerMoveRate == 0:
                self.player.move(self.map)

            self.computerInterval += 1
            
            if self.computerInterval % self.computerPlayRate == 0:
                self.computerInterval = 0
                self.computer.move()
    
    def handleEvents(self, event):
        if not self.gameComplete:
            if event.type == pg.KEYDOWN: # Player can only move in one direction at a time
                if event.key == pg.K_UP:
                    self.player.clearVel()
                    self.player.yVel = -1
                if event.key == pg.K_DOWN:
                    self.player.clearVel()
                    self.player.yVel = 1
                if event.key == pg.K_LEFT:
                    self.player.clearVel()
                    self.player.xVel = -1
                if event.key == pg.K_RIGHT:
                    self.player.clearVel()
                    self.player.xVel = 1
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    if self.player.yVel == -1:
                        self.player.clearVel()
                if event.key == pg.K_DOWN:
                    if self.player.yVel == 1:
                        self.player.clearVel()
                if event.key == pg.K_LEFT:
                    if self.player.xVel == -1:
                        self.player.clearVel()
                if event.key == pg.K_RIGHT:
                    if self.player.xVel == 1:
                        self.player.clearVel()
        else:
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN: # Reset level or proceed to next
                    if self.playerWin:
                        self.currentLevel += 1
                    if self.currentLevel == len(LEVELPATHS):
                        self.parent.running = False
                        return
                    self.startLevel(LEVELPATHS[self.currentLevel])
                
        