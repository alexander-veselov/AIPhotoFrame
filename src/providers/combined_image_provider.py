import logging
import random
from providers.image_provider import ImageProvider

class CombinedImageProvider(ImageProvider):
    def __init__(self, width, height, rotate):
        super().__init__(width, height, rotate)
        self.width = width 
        self.height = height
        self.rotate = rotate
        self.providers = []
    
    def add_provider(self, provider, weight=1.0):
        self.providers.append((weight, provider(self.width, self.height, self.rotate)))

    def provide(self):
        if len(self.providers) == 0:
            logging.error("No providers")
            return None
        weights, values = zip(*self.providers)
        provider = random.choices(values, weights=weights, k=1)[0]
        return provider.provide()