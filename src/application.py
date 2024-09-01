import pygame
import threading
from render import Renderer
from image_provider import ImageProvider
from generators.generator import create_generator
from display.display import create_surface, create_display

class Application:
    def __init__(self, params):
        pygame.init()
        self.running = False
        self.rotate = params.rotate
        self.flip = params.flip
        self.size = (params.width, params.height)
        self.display = create_display(params.display, self.size, params.fullscreen)
        self.image_generator = create_generator(params.generator, params.ip, params.port)
        self.renderer = Renderer(self.display, params.fps, params.frame_duration, params.fade_duration)
        self.image_provider = ImageProvider(
            self.image_generator, params.prompt, params.negative_prompt,
            self.size, params.rotate, params.flip,
            self.renderer.put, self.renderer.full
        )
        self.image_provider_thread = threading.Thread(target=self.image_provider.run, daemon=True)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('AI Photo Frame')

    def run(self):
        self.running = True
        self.image_provider_thread.start()
        while self.running:
            self.process_events(pygame.event.get())
            self.renderer.render()
        self.renderer.reset()
        pygame.quit()
        return 0
    
    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONUP:
                self.running = False