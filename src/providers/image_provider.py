import pygame
from generated_image import GeneratedImage

class ImageProvider:
    def __init__(self, width, height, rotate, flip):
        self.render_size = (height, width) if rotate else (width, height)
        self.rotate = rotate
        self.flip = flip

    def provide(self):
        raise NotImplementedError()
    
    def crop(self, surface: pygame.Surface):
        sw, sh = surface.get_size()
        tw, th = self.render_size
        if (tw > th) != (sw > sh) or sw == sh:
            return None
        scale = max(tw / sw, th / sh)
        new_w, new_h = int(sw * scale), int(sh * scale)
        scaled = pygame.transform.smoothscale(surface, (new_w, new_h))
        left = max(0, (new_w - tw) // 2)
        top = max(0, (new_h - th) // 2)
        cropped = scaled.subsurface(pygame.Rect(left, top, tw, th)).copy()
        return cropped

    def create_image(self, image_data, generation_info):
        original_image = pygame.image.load(image_data)
        image = original_image.copy()
        image = self.crop(image)
        if image is None:
            return None
        if self.rotate:
            image = pygame.transform.rotate(image, -90)
        if self.flip:
            image = pygame.transform.flip(image, flip_x=self.rotate, flip_y=not self.rotate)
        return GeneratedImage(image, original_image, generation_info)