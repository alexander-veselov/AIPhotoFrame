import pygame
from render.render_config import RenderConfig
from render.render_stage import RenderStage
from generated_image import GeneratedImage

class CalibrateStage(RenderStage):
    def __init__(self, render_config: RenderConfig):
        super().__init__(render_config)

    def process(self, image: GeneratedImage) -> GeneratedImage:
        original = image.copy()
        width = self.render_config.width
        height = self.render_config.height
        width_shift = self.render_config.width_shift
        height_shift = self.render_config.height_shift
        if self.render_config.rotate:
            width, height = height, width
            width_shift, height_shift = height_shift, width_shift
        shifted_surface = pygame.Surface((width, height))
        shifted_surface.fill((0, 0, 0))
        shifted_surface.blit(original, (max(0, width_shift), max(0, height_shift)))
        return GeneratedImage(shifted_surface, image.original_image, image.generation_info)
