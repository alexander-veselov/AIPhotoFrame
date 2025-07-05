import pygame
import time
from generated_image import GeneratedImage

class ImageProvider:
    def __init__(self, image_generator, prompt_generator, renderer, prompt, negative_prompt, width, height, rotate, flip, improve_prompt):
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.render_size = (height, width) if rotate else (width, height)
        self.rotate = rotate
        self.flip = flip
        self.image_generator = image_generator
        self.prompt_generator = prompt_generator
        self.renderer = renderer
        self.running = False
        self.improve_prompt = improve_prompt

    def run(self):
        self.running = True
        while self.running:
            if not self.renderer.full():
                image = self.generate_image()
                self.renderer.put(image)
            time.sleep(1)

    def stop(self):
        self.running = False

    def create_image(self, image_data, generation_info):
        image = pygame.image.load(image_data)
        scaled_image = pygame.transform.smoothscale(image, self.render_size)
        return GeneratedImage(self.transform(scaled_image), image, generation_info)

    def generate_image(self):
        prompt, negative_prompt = self.prompt_generator.process(
            self.render_size,
            self.prompt,
            self.negative_prompt,
            self.improve_prompt
        )
    
        image_data, generation_info = self.image_generator.generate(
            self.render_size,
            prompt,
            negative_prompt
        )

        return self.create_image(image_data, generation_info)

    def transform(self, image):
        if self.rotate:
            image = pygame.transform.rotate(image, -90)
        if self.flip:
            image = pygame.transform.flip(image, flip_x=self.rotate, flip_y=not self.rotate)
        return image