import pygame as pg
from playelements import *
from utilities import *
from definitions import *
from os import path

class PlayScreen:
    def __init__(self, parent):
        self.parent = parent
        self.startLevel(0)
    
    def startLevel(self, levelImage):
        self.createMapFromImage(levelImage)
        self.player = Player(self.startLocation[0], self.startLocation[1], TILESIZE)
        path = [[2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8]] # pathfinding
        #from BensPF import Pathfinding
        #pathFinder = Pathfinding(self.map, [self.startLocation[1], self.startLocation[0]], [self.endLocation[1], self.endLocation[0]])
        #path = pathFinder.findPath()

        self.computer = Computer(self.startLocation[0], self.startLocation[1], TILESIZE, path)
        self.camera = Camera(WIDTH, HEIGHT, TILESIZE, self.player, self.map)
        self.mapDisplay = MapDisplay(self.map, TILESIZE)
    
    def createMapFromImage(self, levelImage):
        # TO DO FILL IN PROPERLY
        dir = path.dirname(__file__)
        self.map = []  # empty list to store map data
        with open(path.join(dir, 'mapTest.txt'), 'rt') as f:
            for line in f:
                mapLine = []
                for c in line.rstrip():
                    mapLine.append(c)
                self.map.append(mapLine)  # read in map line-by-line
        
        for row, tiles in enumerate(self.map): # Need to fix this
            for col, tile in enumerate(tiles):
                if tile == '2':
                    self.startLocation = [col, row]
                if tile == '3':
                    self.endLocation = [col, row]

    
    def draw(self, screen):
        screen.fill(BLACK)
        self.camera.moveCamera(self.player)

        self.mapDisplay.draw(screen, self.camera)
        self.computer.draw(screen, self.camera)
        self.player.draw(screen, self.camera)
    
    def update(self):
        self.running = True
    
    def handleEvents(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                if self.player.move(self.map, PLAYER_UP):
                    self.computer.move()
            if event.key == pg.K_DOWN:
                if self.player.move(self.map, PLAYER_DOWN):
                    self.computer.move()
            if event.key == pg.K_LEFT:
                if self.player.move(self.map, PLAYER_LEFT):
                    self.computer.move()
            if event.key == pg.K_RIGHT:
                if self.player.move(self.map, PLAYER_RIGHT):
                    self.computer.move()
                
        