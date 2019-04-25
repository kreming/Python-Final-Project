import pygame as pg
from definitions import *
from titlescreen import *
from playscreen import *


class Game:
    def __init__(self):
        pg.init() # Initialize Pygame (required)
        self.window = pg.display.set_mode((WIDTH, HEIGHT)) # Set window width and height
        pg.display.set_caption(TITLE) # Set window title
        self.clock = pg.time.Clock() # Initialize clock for game loop

        self.screens = [] # Create screens
        self.screens.append(TitleScreen(self)) # Screen id 0 <-- definitions.TITLESCREEN
        self.screens.append(PlayScreen(self)) # Screen id 1
    
    def setScreen(self, newScreenID):
        """
        This function allows the screen to be changed from anywhere where the game object is exposed
        """
        self.currentScreen = self.screens[newScreenID]

    def run(self):
        """
        Main game loop
        """
        self.running = True

        while self.running:
            self.handleEvents()
            self.update()
            self.draw()

            self.clock.tick(FPS) # This ensures framerate will cap at FPS
    
    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: # If player quits, return immediately
                self.running = False
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    return
                
            self.currentScreen.handleEvents(event) # Handle events for currently active screen
    
    def update(self):
        self.currentScreen.update() # Update currently active screen

    def draw(self):
        self.window.fill(BLACK)
        self.currentScreen.draw(self.window) # Draw currently active screen
        pg.display.flip()
        #print(self.clock.get_fps()) #See FPS