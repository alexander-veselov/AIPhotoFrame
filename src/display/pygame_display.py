import pygame

class PygameDisplay:
    def __init__(self, width, height, fullscreen):
        flags = pygame.DOUBLEBUF
        if fullscreen: flags = flags | pygame.FULLSCREEN
        self.surface = pygame.display.set_mode((width, height), flags)

    def get_surface(self):
        return self.surface

    def flip(self):
        pygame.display.flip()

    def reset(self):
        self.surface.fill((255, 255, 255))