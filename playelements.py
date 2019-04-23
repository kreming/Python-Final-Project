import pygame as pg
from definitions import *

class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.trail = []

        # Player draw color
        self.color = YELLOW

        self.relX = None
        self.relX = None
    
    def move(self, map, dir):
        oldPos = [self.x, self.y]
        self.x += dir[0]
        self.y += dir[1]

        if self.x >= len(map[0]) or self.y >= len(map) or map[self.y][self.x] == '1': # Wall
            self.x = oldPos[0]
            self.y = oldPos[1]
            return False # Move computer?
        else:
            self.trail.append([oldPos])
            return True
    
    def checkWin(self, map):
        return map[self.y][self.x] == '3'
    
    def draw(self, screen, camera):
        self.relX = self.x - camera.x
        self.relY = self.y - camera.y

        drawX = self.relX * self.size
        drawY = self.relY * self.size

        pg.draw.rect(screen, self.color, pg.Rect(drawX, drawY, self.size, self.size))

class Computer:
    def __init__(self, x, y, size, path):
        self.x = x
        self.y = y
        self.size = size
        self.path = path

        # Computer draw color
        self.color = BLUE

        self.relX = None
        self.relY = None
    
    def move(self):
        if len(self.path) >= 1: # Spaces left to move
            self.x = self.path[0][0]
            self.y = self.path[0][1]
            self.path = self.path[1:]
    
    def checkWin(self):
        return len(self.path) == 0
    
    def draw(self, screen, camera):
        self.relX = self.x - camera.x
        self.relY = self.y - camera.y

        drawX = self.relX * self.size
        drawY = self.relY * self.size

        pg.draw.rect(screen, self.color, pg.Rect(drawX, drawY, self.size, self.size))
        

class Camera:
    def __init__(self, width, height, tileSize, player, map):
        self.x = -(((width/tileSize) - len(map[0])) / 2)
        self.y = -(((height/tileSize) - len(map)) / 2)
        self.width = width
        self.height = height
        self.tileSize = tileSize
        self.lockX = len(map[0]) <= (width / tileSize)
        self.lockY = len(map) <= (height / tileSize)
        self.maxX = len(map[0]) - (width / tileSize)
        self.maxY = len(map) - (height / tileSize)
    
    def moveCamera(self, player):
        if not self.lockX:
            self.x = player.x - ((self.width / self.tileSize) / 2)
            # Don't pass map edges
            if self.x < 0:
                self.x = 0
            if self.x > self.maxX:
                self.x = self.maxX
        
        if not self.lockY:
            self.y = player.y - ((self.height / self.tileSize) / 2)
            # Don't pass map edges
            if self.y < 0:
                self.y = 0
            if self.y > self.maxY:
                self.y = self.maxY


class TileDisplay:
    def __init__(self, x, y, ID, tileSize):
        self.x = x
        self.y = y
        self.tileSize = tileSize

        if ID == '0':
            self.color = BLACK
        elif ID == '1':
            self.color = LIGHTGREY
        elif ID == '2':
            self.color = RED
        elif ID == '3':
            self.color = GREEN
        else:
            self.color = WHITE

        self.relX = None
        self.relY = None

    def draw(self, screen, camera):
        self.relX = self.x - camera.x
        self.relY = self.y - camera.y

        drawX = self.relX * self.tileSize
        drawY = self.relY * self.tileSize

        pg.draw.rect(screen, self.color, pg.Rect(drawX, drawY, self.tileSize, self.tileSize))

        

class MapDisplay:
    def __init__(self, map, tileSize):
        self.map = map
        self.tiles = []
        for y, row in enumerate(self.map):
            for x, column in enumerate(self.map[y]):
                self.tiles.append(TileDisplay(x, y, self.map[y][x], tileSize))
    
    def draw(self, screen, camera):
        for tile in self.tiles:
            tile.draw(screen, camera)        
