import random
from providers.api_image_provider import ApiImageProvider, ImageResult
from render.render_config import RenderConfig

class WaifupicsImageProvider(ApiImageProvider):
    def __init__(self, render_config: RenderConfig):
        super().__init__(render_config, base_url="https://api.waifu.pics/sfw")

    def request_image(self):
        categories = ['waifu', 'neko']
        category = random.choices(categories, [0.7, 0.3])[0]

        data = self.get_json(category)

        if not data:
            return None

        return ImageResult(
            url=data.get("url"),
            source=None
        )