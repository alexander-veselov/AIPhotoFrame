import pygame
from render.render_pipeline import RenderStage
from generated_image import GeneratedImage

class CalibrateStage(RenderStage):
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def process(self, image: GeneratedImage) -> GeneratedImage:
        original = image.copy()
        width, height = original.get_size()
        shifted_surface = pygame.Surface((width, height))
        shifted_surface.fill((0, 0, 0))
        shifted_surface.blit(original, (self.dx, self.dy))
        return GeneratedImage(shifted_surface, image.original_image, image.generation_info)
