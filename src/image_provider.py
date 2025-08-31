import pygame
import time
import queue
import threading
from io import BytesIO
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

class ConcurrentImageProvider(ImageProvider):
    def __init__(self, width, height, rotate, flip):
        super().__init__(width, height, rotate, flip)
        self.queue = queue.Queue(maxsize=3)
        self.running = False
        self.thread = None

    def provide(self):
        if not self.running:
            self.start()
        try:
            return self.queue.get_nowait()
        except queue.Empty:
            return None
        
    def start(self):
        if not self.thread or not self.thread.is_alive():
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

    def _run(self):
        self.running = True
        while self.running:
            if not self.queue.full():
                image = self.concurrent_provide()
                self.queue.put(image)
            time.sleep(0.5)

    def concurrent_provide(self):
        raise NotImplementedError()

class GeneratedImageProvider(ConcurrentImageProvider):
    def __init__(self, width, height, rotate, flip, image_generator, prompt_generator, prompt, negative_prompt, improve_prompt):
        super().__init__(width, height, rotate, flip)
        self.image_generator = image_generator
        self.prompt_generator = prompt_generator
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.improve_prompt = improve_prompt

    def concurrent_provide(self):
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

class MockImageProvider(ImageProvider):
    def __init__(self, width, height, rotate, flip):
        super().__init__(width, height, rotate, flip)
        self.image_index = -1
        self.type = "horizontal" if self.render_size[0] > self.render_size[1] else "vertical"
        self.images = [
            self._read(self.type + "/1.bin"),
            self._read(self.type + "/2.bin")
        ]

    def provide(self):
        self.image_index = (self.image_index + 1) % len(self.images)
        return self.create_image(BytesIO(self.images[self.image_index]), f"Mock image #{self.image_index}")
    
    def _read(self, image_name):
        with open("data/" + image_name, 'rb') as file:
            return file.read()