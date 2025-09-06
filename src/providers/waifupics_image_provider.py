import requests
import random
from io import BytesIO
from PIL import Image
from providers.image_provider import ImageProvider

class WaifupicsImageProvider(ImageProvider):
    def __init__(self, width, height, rotate):
        super().__init__(width, height, rotate)

    def request_image(self):
        categories = ['waifu', 'neko']
        category = random.choices(categories, [0.7, 0.3])[0]
        type = 'sfw'
        api = f'https://api.waifu.pics/{type}/{category}'
        response = requests.get(api)
        if response.status_code != 200:
            print("waifu.pics response error: {0}".format(response.status_code))
            return None
        return response.json()['url']
    
    def download_image(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return BytesIO(response.content)

    def provide(self):
        image_url = self.request_image()
        if image_url is None:
            return None
        image_data = self.download_image(image_url)
        if image_data is None:
            return None
        return self.create_image(image_data, image_url)