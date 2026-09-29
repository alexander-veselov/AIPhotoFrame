import logging
import random
from providers.api_image_provider import ApiImageProvider, ImageResult
from render.render_config import RenderConfig

class NekosBestImageProvider(ApiImageProvider):
    def __init__(self, render_config: RenderConfig):
        super().__init__(render_config, base_url="https://nekos.best/api/v2")

    def request_image(self):
        categories = ["waifu", "neko", "kitsune"]
        weights = [0.6, 0.2, 0.1]

        category = random.choices(categories, weights)[0]

        data = self.get_json(category)

        if not data:
            return None

        try:
            item = data["results"][0]
            return ImageResult(
                url=item["url"],
                source=item.get("source_url", None)
            )
        except (KeyError, IndexError):
            logging.error("nekos.best invalid response format")
            return None