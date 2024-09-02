import pygame

class PygameDisplay:
    def __init__(self, surface):
        self.surface = surface

    def get_surface(self):
        return self.surface

    def flip(self):
        pygame.display.flip()

    def reset(self):
        self.surface.fill((255, 255, 255))