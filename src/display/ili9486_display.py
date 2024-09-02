import pygame
from PIL import Image
from spidev import SpiDev
from ili9486.ili9486 import ILI9486

class ILI9486Display:
    def __init__(self, surface):
        self.surface = surface
        self.spi = SpiDev(0, 0)
        self.spi.mode = 0b10
        self.spi.max_speed_hz = 48000000
        self.driver = ILI9486(dc=24, rst=25, spi=self.spi)

    def get_surface(self):
        return self.surface

    def flip(self):
        pixel_array = pygame.surfarray.array3d(self.surface)
        image = Image.fromarray(pixel_array.swapaxes(0, 1), 'RGB')
        image = image.crop((0, 0, *self.driver.get_size()))
        self.driver.display(image)
    
    def reset(self):
        self.driver.reset()