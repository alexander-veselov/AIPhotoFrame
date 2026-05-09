import random
import logging
from providers.api_image_provider import ApiImageProvider, ImageResult

class DanbooruImageProvider(ApiImageProvider):
    def __init__(self, width, height, rotate):
        super().__init__(width, height, rotate, base_url="https://danbooru.donmai.us")

    def request_image(self):
        params = {
            "tags": "rating:g score:>100 1girl looking_at_viewer",
        }

        data = self.get_json("posts/random", params=params)

        if not data:
            return None

        try:
            post = data

            if post.get('file_ext') == 'mp4':
                return None

            url = post.get("file_url") or post.get("large_file_url")
            if not url:
                return None

            return ImageResult(
                url=url,
                source=f"https://danbooru.donmai.us/posts/{post['id']}"
            )

        except (KeyError, IndexError):
            logging.error("Danbooru invalid response format")
            return None