import queue
import pygame

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

class CompositeRenderer:
    def __init__(self):
        self.queue = queue.Queue()
        self.current_renderer = EmptyRenderer()
    
    def put(self, renderer):
        self.queue.put(renderer)

    def is_running(self):
        return not self.queue.empty() or self.current_renderer.is_running()
    
    def render(self):
        if not self.current_renderer.is_running() and not self.queue.empty():
            self.current_renderer = self.queue.get()
        self.current_renderer.render()

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

    def full(self):
        return self.queue.full()

    def put(self, image):
        self.queue.put(image)

    def render(self): 
        if not self.renderer.is_running():
            current_image = self.image
            if not self.queue.empty():
                self.image = self.queue.get()
                self.renderer = CompositeRenderer()
                if current_image is not None:
                    self.renderer.put(FadeRenderer(self.screen, self.fps, current_image, self.image, self.fade_duration))
                self.renderer.put(StaticRenderer(self.screen, self.fps, self.image, self.frame_duration))
        self.renderer.render()
        pygame.display.flip()
        self.clock.tick(self.fps)