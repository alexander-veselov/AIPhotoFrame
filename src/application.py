import pygame
import threading

class Application:
    def __init__(self, renderer, image_provider):
        pygame.init()
        pygame.display.set_caption('AI Photo Frame')
        pygame.mouse.set_visible(False)
        self.renderer = renderer
        self.image_provider_thread = threading.Thread(target=image_provider.run, daemon=True)

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
            if event.type == pygame.QUIT or \
               event.type == pygame.MOUSEBUTTONDOWN or \
               event.type == pygame.KEYDOWN:
                self.running = False