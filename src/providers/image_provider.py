import pygame
from generated_image import GeneratedImage

class ImageProvider:
    def __init__(self, width, height, rotate, flip):
        self.render_size = (height, width) if rotate else (width, height)
        self.rotate = rotate
        self.flip = flip

    def provide(self):
        raise NotImplementedError()

    def create_image(self, image_data, generation_info):
        image = pygame.image.load(image_data)
        image = pygame.transform.smoothscale(image, self.render_size)
        if self.rotate:
            image = pygame.transform.rotate(image, -90)
        if self.flip:
            image = pygame.transform.flip(image, flip_x=self.rotate, flip_y=not self.rotate)
        return GeneratedImage(image, image, generation_info)