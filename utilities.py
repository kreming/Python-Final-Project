import pygame as pg

images = {}
def get_image(filePath):
        """
        Load images only once and store them once they are loaded
        """
        global images
        image = images.get(filePath)
        if image == None: # Image is not yet loaded, load now
                image = pg.image.load('Assets/'+filePath)
                images[filePath] = image
        return image