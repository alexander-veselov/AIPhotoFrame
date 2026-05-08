import random
from providers.api_image_provider import ApiImageProvider, ImageResult

class WaifuimImageProvider(ApiImageProvider):
    def __init__(self, width, height, rotate):
        super().__init__(width, height, rotate, base_url="https://api.waifu.im")

    def request_image(self):
        tags = ["waifu", "uniform", "maid"]
        weights = [0.45, 0.4, 0.15]

        tag = random.choices(tags, weights)[0]

        params = {
            "IsNsfw": "False",
            "Orientation": "Portrait",
            "PageSize": 1,
            "IncludedTags": tag
        }

        data = self.get_json("images", params=params)

        if not data:
            return None

        try:
            return ImageResult(
                url=data["items"][0]["url"],
                source=data["items"][0].get("source", None)
            )
        except (KeyError, IndexError):
            print("waifu.im invalid response format")
            return None