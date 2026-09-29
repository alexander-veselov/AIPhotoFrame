import pygame
from render.render_config import RenderConfig
from render.render_stage import RenderStage
from generated_image import GeneratedImage

class FlipAndRotateStage(RenderStage):
    def __init__(self, render_config: RenderConfig):
        super().__init__(render_config)

    def process(self, image: GeneratedImage) -> GeneratedImage:
        transformed = image.copy()
        if self.render_config.rotate:
            transformed = pygame.transform.rotate(transformed, -90)
        if self.render_config.flip:
            transformed = pygame.transform.flip(transformed, flip_x=self.render_config.rotate, flip_y=not self.render_config.rotate)
        return GeneratedImage(transformed, image.original_image, image.generation_info)
