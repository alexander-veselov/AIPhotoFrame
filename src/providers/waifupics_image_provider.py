import random
from providers.api_image_provider import ApiImageProvider

class WaifupicsImageProvider(ApiImageProvider):
    def __init__(self, width, height, rotate):
        super().__init__(width, height, rotate, base_url="https://api.waifu.pics/sfw")

    def request_image_url(self):
        categories = ['waifu', 'neko']
        category = random.choices(categories, [0.7, 0.3])[0]

        data = self.get_json(category)

        if not data:
            return None

        return data.get("url")