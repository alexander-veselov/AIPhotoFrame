import pygame
from PIL import Image, ImageChops
from inky.auto import auto

class InkyDisplay:
    def __init__(self, width, height):
        self.surface = pygame.Surface((width, height))
        self.display = auto()
        self.last_image = None

    def get_surface(self):
        return self.surface

    def flip(self):
        pixel_data = pygame.image.tostring(self.surface, 'RGB')
        image = Image.frombytes('RGB', self.surface.get_size(), pixel_data)
        image = image.crop((0, 0, *self.display.resolution))
        if self.last_image is None:
            self.last_image = image
        diff = ImageChops.difference(self.last_image, image)
        if diff.getbbox():
            self.last_image = image
            self.display.set_image(image)
            self.display.show()
    
    def reset(self):
        pass # TODO: implement if needed