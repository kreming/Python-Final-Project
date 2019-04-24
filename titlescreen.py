import pygame as pg
from definitions import *
from utilities import *

class Button:
    def __init__(self, imagePath, rect, onClick):
        self.image = get_image(imagePath)
        self.rect = rect
        self.onClick = onClick
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def clicked(self, game):
        self.onClick()

class TitleScreen:
    def __init__(self, parent):
        self.running = True
        self.parent = parent
        self.buttons = []

        def advanceScreens():
            parent.setScreen(PLAYSCREEN)

        self.buttons.append(Button('playBtn.png', pg.Rect(100, 100, 309, 128),  advanceScreens))

    def draw(self, screen):
        if self.running:
            pg.draw.rect(screen, (0, 128, 255), pg.Rect(30, 30, 60, 60))
            self.buttons[0].draw(screen)
    
    def update(self):
        self.running = True
    
    def mouseClick(self, pos):
        buttons = [b for b in self.buttons if b.rect.collidepoint(pos)]
        for b in buttons:
            b.clicked(self.parent)
    
    def handleEvents(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.running = not self.running
        
        if event.type == pg.MOUSEBUTTONUP:
            self.mouseClick(pg.mouse.get_pos())

