import pygame
from stable_diffusion import StableDiffusion

class Application:
    def __init__(self, params):
        pygame.init()
        self.running = False
        self.rotate = params.rotate
        self.flip = params.flip
        self.prompt = params.prompt
        self.negative_prompt = params.negative_prompt
        self.render_size = (params.height, params.width) if params.rotate else (params.width, params.height)
        self.image_generator = StableDiffusion(params.ip, params.port, self.render_size)
        self.screen = pygame.display.set_mode(
            (params.width, params.height),
            pygame.FULLSCREEN if params.windowed else 0
        )
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('AI Photo Frame')

    def run(self):
        self.reneder_welcome_screen()
        pygame.display.flip()

        self.running = True
        while self.running:
            self.process_events(pygame.event.get())
            self.render()

        pygame.quit()
        return 0
    
    def render(self):
        image_data = self.image_generator.generate(self.prompt, self.negative_prompt)
        self.render_image(image_data)
        pygame.display.flip()
    
    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONUP:
                self.running = False
        
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