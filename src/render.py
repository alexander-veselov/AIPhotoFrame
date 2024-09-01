import queue
import pygame
from threading import Lock

class EmptyRenderer:
    def render(self):
        pass

    def is_running(self):
        return False

class StaticRenderer:
    def __init__(self, surface, fps, image, duration):
        self.surface = surface
        self.image = image
        self.frame = 0
        self.total_frames = fps * duration

    def is_running(self):
        return self.frame < self.total_frames

    def render(self):
        self.frame += 1
        self.surface.blit(self.image, (0, 0))

class FadeRenderer:
    MAX_TRANSPARENCY = 255

    def __init__(self, surface, fps, image1, image2, duration):
        self.surface = surface
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
            self.surface.blit(self.image1, (0, 0))
            self.image2.set_alpha(int(self.alpha))
            self.surface.blit(self.image2, (0, 0))

class Renderer:
    RENDER_QUEUE_SIZE = 3

    def __init__(self, display, fps, frame_duration, fade_duration):
        self.display = display
        self.queue = queue.Queue(Renderer.RENDER_QUEUE_SIZE)
        self.fps = fps
        self.frame_duration = frame_duration
        self.fade_duration = fade_duration
        self.renderer = EmptyRenderer()
        self.clock = pygame.time.Clock()
        self.image = None
        self.mutex = Lock()

    def full(self):
        return self.queue.full()

    def put(self, image):
        with self.mutex:
            previous_image = self.image
            self.image = image
            surface = self.display.get_surface()
            if previous_image is not None:
                self.queue.put(FadeRenderer(surface, self.fps, previous_image, self.image, self.fade_duration))
            self.queue.put(StaticRenderer(surface, self.fps, self.image, self.frame_duration))

    def render(self): 
        if not self.renderer.is_running():  
            if not self.queue.empty():
                self.renderer = self.queue.get()
        self.renderer.render()
        self.display.flip()
        self.clock.tick(self.fps)
    
    def reset(self):
        self.display.reset()