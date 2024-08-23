import time
import pygame
import threading
from stable_diffusion import StableDiffusion

class RenderPipeline:
    def __init__(self, screen, frame_display_time, callback):
        self.screen = screen
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

    def reneder_welcome_screen(self):
        # TODO: move somewhere
        pink = (255, 192, 203)
        white = (255, 255, 255)
        self.screen.fill(pink)
        font = pygame.font.SysFont("Cantarell", 74)
        text = font.render("Hello nya!", True, white)
        text_rect = text.get_rect()
        text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2.5)
        self.screen.blit(text, text_rect)

class ImageProvider:
    FADE_DURATION = 5

    def __init__(self, generator, prompt, negative_prompt, render_size, rotate, flip):
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.render_size = render_size
        self.rotate = rotate
        self.flip = flip
        self.generator = generator
        self.image = None

    def create_image(self, image_data):
        image = pygame.image.load(image_data)
        image = pygame.transform.smoothscale(image, self.render_size)
        if self.rotate:
            image = pygame.transform.rotate(image, 90)
        if self.flip:
            image = pygame.transform.flip(image, flip_x=self.rotate, flip_y=not self.rotate)
        return image

    def generate_image(self):
        image_data = self.generator.generate(self.prompt, self.negative_prompt)
        return self.create_image(image_data)

    def render(self, renderer):
        screen = renderer.screen
        if self.image is None:
            self.image = self.generate_image()
            screen.blit(self.image, (0, 0))
        else:
            # TODO: remove magic constants
            # TODO: create "fade" param
            # TODO: fix crash on app exit while transition
            clock = pygame.time.Clock()
            new_image = self.generate_image()
            alpha = 0
            while alpha < 255:
                alpha += 255 / (ImageProvider.FADE_DURATION * 60)
                self.image.set_alpha(255 - int(alpha))
                screen.blit(self.image, (0, 0))
                new_image.set_alpha(int(alpha))
                screen.blit(new_image, (0, 0))
                clock.tick(30)
            self.image = new_image

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
        self.image_provider = ImageProvider(
            self.image_generator, params.prompt,
            params.negative_prompt, self.render_size,
            params.rotate, params.flip
        )
        self.render_pipeline = RenderPipeline(
            self.screen, params.frame_display_time,
            self.image_provider.render
        )
        self.render_thread = threading.Thread(
            target=self.render_pipeline.render, daemon=True
        )
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