import pygame
import threading
from image_saver import ImageSaver

class Application:
    def __init__(self, renderer, image_provider):
        pygame.init()
        pygame.display.set_caption('AI Photo Frame')
        pygame.mouse.set_visible(False)
        self.renderer = renderer
        self.image_provider = image_provider
        self.image_provider_thread = threading.Thread(target=image_provider.run, daemon=True)
        self.image_saver = ImageSaver()

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
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.process_key_event(event)

    def process_key_event(self, event):
        if event.key == pygame.K_a or event.key == pygame.K_PRINTSCREEN:
            image = self.renderer.get_image()
            self.image_saver.save_image(image)
        elif event.key == pygame.K_d or event.key == pygame.K_SPACE:
            self.renderer.next_image()