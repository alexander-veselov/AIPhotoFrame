import pygame

class GeneratedImage(pygame.Surface):
    def __init__(self, surface: pygame.Surface, generation_info: str = ""):
        pygame.Surface.__init__(self, surface.get_size(), surface.get_flags(), surface.get_bitsize())
        self.blit(surface, (0, 0))
        self.generation_info = generation_info