import pygame
import time

class ImageProvider:
    def __init__(self, generator, renderer, prompt, negative_prompt, width, height, rotate, flip):
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.render_size = (height, width) if rotate else (width, height)
        self.rotate = rotate
        self.flip = flip
        self.generator = generator
        self.renderer = renderer
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            if not self.renderer.full():
                self.renderer.put(self.generate_image())
            time.sleep(1)

    def stop(self):
        self.running = False

    def create_image(self, image_data):
        image = pygame.image.load(image_data)
        image = pygame.transform.smoothscale(image, self.render_size)
        if self.rotate:
            image = pygame.transform.rotate(image, -90)
        if self.flip:
            image = pygame.transform.flip(image, flip_x=self.rotate, flip_y=not self.rotate)
        return image

    def generate_image(self):
        image_data = self.generator.generate(self.render_size, self.prompt, self.negative_prompt)
        return self.create_image(image_data)