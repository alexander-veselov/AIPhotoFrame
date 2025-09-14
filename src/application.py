import pygame
from image_saver import ImageSaver
from render.render_pipeline import RenderPipeline

class Application:
    def __init__(self, config, renderer, image_provider):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('AI Photo Frame')
        pygame.mouse.set_visible(False)
        self.config = config
        self.image_saver = ImageSaver()
        self.renderer = renderer
        self.image_provider = image_provider
        self.render_pipeline = RenderPipeline.from_config(config)

    def run(self):
        self.running = True
        while self.running:
            self.process_events(pygame.event.get())
            if self.renderer.is_idle():
                image = self.image_provider.provide()
                if image is not None:
                    processed_image = self.render_pipeline.process(image)
                    self.renderer.put(processed_image)
            self.renderer.render()
        self.renderer.reset()
        pygame.quit()
        return 0

    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.process_key_event(event)

    def process_key_event(self, event):
        if event.key == pygame.K_F1 or event.key == pygame.K_PRINTSCREEN:
            image = self.renderer.get_image()
            self.image_saver.save_image(image)
        elif event.key == pygame.K_F3:
            self.config['dashboard'] = not self.config['dashboard']
            self.render_pipeline = RenderPipeline.from_config(self.config)
            self.renderer.next_image()
        elif event.key == pygame.K_F4 or event.key == pygame.K_SPACE:
            self.renderer.next_image()