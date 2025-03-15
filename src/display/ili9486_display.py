import pygame
from spidev import SpiDev
from ili9486.ili9486 import ILI9486
from utils import surface_to_image

class ILI9486Display:
    def __init__(self, width, height):
        self.surface = pygame.Surface((width, height))
        self.spi = SpiDev(0, 0)
        self.spi.mode = 0b10
        self.spi.max_speed_hz = 48000000
        self.driver = ILI9486(dc=24, rst=25, spi=self.spi)

    def get_surface(self):
        return self.surface

    def flip(self):
        image = surface_to_image(self.surface)
        image = image.crop((0, 0, *self.driver.get_size()))
        self.driver.display(image)
    
    def reset(self):
        self.driver.reset()