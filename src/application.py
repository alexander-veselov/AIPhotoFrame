import pygame
import threading
from render import Renderer
from image_provider import ImageProvider
from stable_diffusion import StableDiffusion

class Application:
    def __init__(self, params):
        pygame.init()
        self.running = False
        self.rotate = params.rotate
        self.flip = params.flip
        self.render_size = (params.height, params.width) if params.rotate else (params.width, params.height)
        self.screen = pygame.display.set_mode(
            (params.width, params.height),
            pygame.DOUBLEBUF | (pygame.FULLSCREEN if params.windowed else 0)
        )
        self.image_generator = StableDiffusion(
            params.ip, params.port, self.render_size
        )
        self.renderer = Renderer(self.screen, params.fps, params.frame_duration, params.fade_duration)
        self.image_provider = ImageProvider(
            self.image_generator, params.prompt, params.negative_prompt,
            self.render_size, params.rotate, params.flip,
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
        pygame.quit()
        return 0
    
    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONUP:
                self.running = False