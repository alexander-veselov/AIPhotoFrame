import time
import pygame
import threading
from stable_diffusion import StableDiffusion

class RenderPipeline:
    def __init__(self, screen, render_size, rotate, flip, frame_display_time, callback):
        self.screen = screen
        self.render_size = render_size
        self.rotate = rotate
        self.flip = flip
        self.frame_display_time = frame_display_time
        self.callback = callback
        self.running = False

    def render(self):
        self.running = True
        self.reneder_welcome_screen()
        while self.running:
            frame_start_time = time.time()
            self.render_frame()
            frame_end_time = time.time()
            frame_duration = frame_end_time - frame_start_time
            if frame_duration < self.frame_display_time:
                time.sleep(self.frame_display_time - frame_duration)

    def render_frame(self):
        self.callback(self)

    def render_image(self, image_data):
        image = pygame.image.load(image_data)
        image = pygame.transform.smoothscale(image, self.render_size)
        if self.rotate:
            image = pygame.transform.rotate(image, 90)
        if self.flip:
            image = pygame.transform.flip(image, flip_x=self.rotate, flip_y=not self.rotate)
        self.screen.blit(image, (0, 0))

    def reneder_welcome_screen(self):
        pink = (255, 192, 203)
        white = (255, 255, 255)
        self.screen.fill(pink)
        font = pygame.font.SysFont("Cantarell", 74)
        text = font.render("Hello nya!", True, white)
        text_rect = text.get_rect()
        text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2.5)
        self.screen.blit(text, text_rect)

class ImageProvider:
    def __init__(self, generator, prompt, negative_prompt):
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.generator = generator

    def render(self, renderer):
        image_data = self.generator.generate(self.prompt, self.negative_prompt)
        renderer.render_image(image_data)

class Application:
    def __init__(self, params):
        pygame.init()
        self.running = False
        self.rotate = params.rotate
        self.flip = params.flip
        self.render_size = (params.height, params.width) if params.rotate else (params.width, params.height)
        self.screen = pygame.display.set_mode(
            (params.width, params.height),
            pygame.FULLSCREEN if params.windowed else 0
        )
        self.image_generator = StableDiffusion(params.ip, params.port, self.render_size)
        self.image_provider = ImageProvider(self.image_generator, params.prompt, params.negative_prompt)
        self.render_pipeline = RenderPipeline(
            self.screen, self.render_size,
            params.rotate, params.flip, params.frame_display_time,
            self.image_provider.render
        )
        self.render_thread = threading.Thread(target=self.render_pipeline.render, daemon=True)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('AI Photo Frame')

    def run(self):
        self.running = True
        self.render_thread.start()
        while self.running:
            self.process_events(pygame.event.get())
            pygame.display.flip()
        pygame.quit()
        return 0
    
    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONUP:
                self.running = False