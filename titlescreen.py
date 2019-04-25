import pygame as pg
from definitions import *
from utilities import *

class Button:
    """
    Button class used to add interactive buttons to the screen
    """
    def __init__(self, imagePath, imageHoveredPath, rect, onClick):
        self.image = get_image(imagePath)
        self.image_hovered = get_image(imageHoveredPath) # What the button will look like when the mouse is above it
        self.rect = rect
        self.onClick = onClick
        self.hovered = False

    def draw(self, screen):
        if not self.hovered:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image_hovered, self.rect)
    
    def clicked(self, game):
        self.onClick()

class TitleScreen:
    """
    Title screen is the first screen showed when the game starts, gives the player instructions
    """
    def __init__(self, parent):
        self.parent = parent
        self.bgImage = get_image('pathfinderMenu.jpg')
        self.buttons = []

        def advanceScreens():
            parent.setScreen(PLAYSCREEN)
        
        def stopGame():
            parent.running = False

        self.buttons.append(Button('playBtn.jpg', 'playBtn_hover.jpg', pg.Rect(58, 622, 237, 64),  advanceScreens))
        self.buttons.append(Button('exitBtn.jpg', 'exitBtn_hover.jpg', pg.Rect(715, 615, 240, 67), stopGame))

    def draw(self, screen):
        screen.blit(self.bgImage, pg.Rect(0, 0, WIDTH, HEIGHT)) # Draw background
        for b in self.buttons: # Draw buttons
            b.draw(screen)
    
    def update(self):
        pos = pg.mouse.get_pos()
        for b in self.buttons: # Check if buttons are hovered
            b.hovered = False
            if b.rect.collidepoint(pos):
                b.hovered = True
    
    def mouseClick(self, pos):
        buttons = [b for b in self.buttons if b.rect.collidepoint(pos)] # Process button clicks
        for b in buttons:
            b.clicked(self.parent)
    
    def handleEvents(self, event):
        if event.type == pg.MOUSEBUTTONUP: # Mouse click
            self.mouseClick(pg.mouse.get_pos())

