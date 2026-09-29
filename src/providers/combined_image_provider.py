import logging
import random
from providers.image_provider import ImageProvider
from render.render_config import RenderConfig

class CombinedImageProvider(ImageProvider):
    def __init__(self, render_config: RenderConfig):
        super().__init__(render_config)
        self.providers = []
    
    def add_provider(self, provider, weight=1.0):
        self.providers.append((weight, provider(self.render_config)))

    def provide(self):
        if len(self.providers) == 0:
            logging.error("No providers")
            return None
        weights, values = zip(*self.providers)
        provider = random.choices(values, weights=weights, k=1)[0]
        return provider.provide()