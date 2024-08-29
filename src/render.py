import queue
import pygame
from threading import Lock

from PIL import Image
import RPi.GPIO as GPIO
from spidev import SpiDev
import ILI9486 as LCD

class EmptyRenderer:
    def render(self):
        pass

    def is_running(self):
        return False

class StaticRenderer:
    def __init__(self, screen, fps, image, duration):
        self.screen = screen
        self.image = image
        self.frame = 0
        self.total_frames = fps * duration

    def is_running(self):
        return self.frame < self.total_frames

    def render(self):
        self.frame += 1
        self.screen.blit(self.image, (0, 0))

class FadeRenderer:
    MAX_TRANSPARENCY = 255

    def __init__(self, screen, fps, image1, image2, duration):
        self.screen = screen
        self.image1 = image1
        self.image2 = image2
        self.alpha = 0
        self.step = FadeRenderer.MAX_TRANSPARENCY / ((duration * fps) if duration != 0 else 1)

    def is_running(self):
        return self.alpha < FadeRenderer.MAX_TRANSPARENCY
    
    def render(self):
        if self.is_running():
            self.alpha += self.step
            self.image1.set_alpha(FadeRenderer.MAX_TRANSPARENCY - int(self.alpha))
            self.screen.blit(self.image1, (0, 0))
            self.image2.set_alpha(int(self.alpha))
            self.screen.blit(self.image2, (0, 0))

class Renderer:
    RENDER_QUEUE_SIZE = 3

    def __init__(self, screen, fps, frame_duration, fade_duration):
        self.screen = screen
        self.queue = queue.Queue(Renderer.RENDER_QUEUE_SIZE)
        self.fps = fps
        self.frame_duration = frame_duration
        self.fade_duration = fade_duration
        self.renderer = EmptyRenderer()
        self.clock = pygame.time.Clock()
        self.image = None
        self.mutex = Lock()

        # TODO: refactor
        self.spi = SpiDev(0, 0)
        self.spi.mode = 0b10
        self.spi.max_speed_hz = 36000000
        self.lcd = LCD.ILI9486(dc=24, rst=25, spi=self.spi)

    def full(self):
        return self.queue.full()

    def put(self, image):
        with self.mutex:
            previous_image = self.image
            self.image = image
            if previous_image is not None:
                self.queue.put(FadeRenderer(self.screen, self.fps, previous_image, self.image, self.fade_duration))
            self.queue.put(StaticRenderer(self.screen, self.fps, self.image, self.frame_duration))

    def render(self): 
        if not self.renderer.is_running():  
            if not self.queue.empty():
                self.renderer = self.queue.get()
        self.renderer.render()
        pygame.display.flip()
        self.render_on_display()
        self.clock.tick(self.fps)

    def render_on_display(self):
        pixel_array = pygame.surfarray.array3d(self.screen)
        image = Image.fromarray(pixel_array, 'RGB')
        image = image.rotate(90, expand=True)
        image = image.crop((0, 0, *self.screen.get_size()))
        self.lcd.display(image)
    
    def reset(self):
        self.lcd.reset()