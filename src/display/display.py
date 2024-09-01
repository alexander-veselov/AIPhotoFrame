import pygame
from PIL import Image
from spidev import SpiDev
from .ILI9486 import ILI9486

class PygameDisplay:
    def __init__(self, surface):
        self.surface = surface

    def get_surface(self):
        return self.surface

    def flip(self):
        pygame.display.flip()

    def reset(self):
        self.surface.fill((255, 255, 255))

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
        image = Image.fromarray(pixel_array, 'RGB')
        image = image.rotate(90, expand=True)
        image = image.crop((0, 0, *self.surface.get_size()))
        self.driver.display(image)
    
    def reset(self):
        self.driver.reset()

class CombinedDisplay:
    def __init__(self):
        self.displays = []

    def get_surface(self):
        if len(self.displays) == 0:
            raise Exception("No displays provided")
        return self.displays[0].get_surface()

    def append(self, display):
        self.displays.append(display)

    def flip(self):
        for display in self.displays:
            display.flip()

    def reset(self):
        for display in self.displays:
            display.reset()

def create_surface(display, size, windowed):
    if "pygame" in display:
        return pygame.display.set_mode(
            size,
            pygame.DOUBLEBUF | (pygame.FULLSCREEN if windowed else 0)
        )
    else:
        return pygame.Surface(size)

def create_display(display, surface):
    combined_display = CombinedDisplay()
    for display_name in display.split('+'):
        try:
            if display_name == "ili9486":
                combined_display.append(ILI9486Display(surface))
            elif display_name == "pygame":
                combined_display.append(PygameDisplay(surface))
            else:
                raise Exception("Unsupported display type")
        except Exception as e:
            print('Failed to create "{0}" display'.format(display_name))
            print(e)
    return combined_display