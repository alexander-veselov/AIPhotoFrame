import pygame
import gpiod
import gpiodevice
from enum import IntEnum
from PIL import ImageChops
from utils import surface_to_image
from inky.auto import auto
from gpiod.line import Bias, Direction, Edge

class Buttons(IntEnum):
    A = 5
    B = 6
    C = 16
    D = 24

def to_pygame_button(button):
    if button == Buttons.A:
        return pygame.K_a
    elif button == Buttons.B:
        return pygame.K_b
    elif button == Buttons.C:
        return pygame.K_c
    elif button == Buttons.D:
        return pygame.K_d
    else:
        raise Exception('Wrong button: ' + str(button))

def post_pygame_key_event(button):
    key_event = pygame.event.Event(pygame.KEYDOWN, {'key': to_pygame_button(button)})
    pygame.event.post(key_event)

class EventHandler:
    def __init__(self):
        self.buttons = [Buttons.A, Buttons.B, Buttons.C, Buttons.D]
        self.chip = gpiodevice.find_chip_by_platform()
        self.offsets = [self.chip.line_offset_from_id(id) for id in self.buttons]
        self.input = gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP, edge_detection=Edge.FALLING)
        self.line_config = dict.fromkeys(self.offsets, self.input)
        self.request = self.chip.request_lines(consumer='inky7-buttons', config=self.line_config)

    def process(self):
        timeout = 0.1
        if self.request.wait_edge_events(timeout):
            for event in self.request.read_edge_events():
                index = self.offsets.index(event.line_offset)
                button = self.buttons[index]
                post_pygame_key_event(button)

class InkyDisplay:
    def __init__(self, width, height):
        self.surface = pygame.Surface((width, height))
        self.display = auto()
        self.last_image = None
        self.event_handler = EventHandler()

    def get_surface(self):
        return self.surface

    def flip(self):
        image = surface_to_image(self.surface)
        image = image.crop((0, 0, *self.display.resolution))
        if self.last_image is None:
            self.last_image = image
        diff = ImageChops.difference(self.last_image, image)
        if diff.getbbox():
            self.last_image = image
            self.display.set_image(image)
            self.display.show()
        self.event_handler.process() # TODO: refactor
    
    def reset(self):
        pass # TODO: implement if needed