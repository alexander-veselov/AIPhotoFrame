import pygame
from render.render_stage import RenderStage
from generated_image import GeneratedImage

class CalibrateStage(RenderStage):
    def __init__(self, shift_x: int, shift_y: int):
        self.shift_x = shift_x
        self.shift_y = shift_y

    def process(self, image: GeneratedImage) -> GeneratedImage:
        original = image.copy()
        width, height = original.get_size()
        shifted_surface = pygame.Surface((width, height))
        shifted_surface.fill((0, 0, 0))
        shifted_surface.blit(original, (self.shift_x, self.shift_y))
        return GeneratedImage(shifted_surface, image.original_image, image.generation_info)
