import pygame
from render.render_stage import RenderStage
from generated_image import GeneratedImage

class FlipAndRotateStage(RenderStage):
    def __init__(self, flip, rotate):
        self.flip = flip
        self.rotate = rotate

    def process(self, image: GeneratedImage) -> GeneratedImage:
        transformed = image.copy()
        if self.rotate:
            transformed = pygame.transform.rotate(transformed, -90)
        if self.flip:
            transformed = pygame.transform.flip(transformed, flip_x=self.rotate, flip_y=not self.rotate)
        return GeneratedImage(transformed, image.original_image, image.generation_info)
