import pygame

class GeneratedImage(pygame.Surface):
    def __init__(self, scaled_image: pygame.Surface, original_image: pygame.Surface, generation_info: str = ""):
        pygame.Surface.__init__(self, scaled_image.get_size(), scaled_image.get_flags(), scaled_image.get_bitsize())
        self.blit(scaled_image, (0, 0))
        self.original_image = original_image
        self.generation_info = generation_info