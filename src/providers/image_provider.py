import pygame
from generated_image import GeneratedImage

class ImageProvider:
    def __init__(self, width, height, rotate):
        self.render_size = (height, width) if rotate else (width, height)

    def provide(self):
        raise NotImplementedError()
    
    def crop(self, surface: pygame.Surface):
        if (self.render_size[0] > self.render_size[1]) != (surface.get_width() > surface.get_height()) or \
            surface.get_width() == surface.get_height():
            print("Wrong orientation")
            return None
        scale = max(self.render_size[0] / surface.get_width(), self.render_size[1] / surface.get_height())
        scaled = pygame.transform.smoothscale(surface, (round(surface.get_width() * scale), round(surface.get_height() * scale)))
        left = abs(self.render_size[0] - scaled.get_width()) // 2
        top = abs(self.render_size[1] - scaled.get_height()) // 2
        right = left + self.render_size[0]
        bottom = top + self.render_size[1]
        if left >= right or top >= bottom:
            return None
        cropped = scaled.subsurface(pygame.Rect(left, top, right - left, bottom - top))
        return cropped.copy()

    def create_image(self, image_data, generation_info):
        original_image = pygame.image.load(image_data)
        image = original_image.copy()
        image = self.crop(image)
        if image is None:
            return None
        return GeneratedImage(image, original_image, generation_info)