import requests
import random
from io import BytesIO
from PIL import Image
from providers.image_provider import ImageProvider

class WaifupicsImageProvider(ImageProvider):
    def __init__(self, width, height, rotate, flip):
        super().__init__(width, height, rotate, flip)

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
    
    def crop(self, image_data):
        image = Image.open(BytesIO(image_data.getbuffer()))
        if (self.render_size[0] > self.render_size[1]) != (image.width > image.height) or image.width == image.height:
            return None
        scale = max(self.render_size[0] / image.width, self.render_size[1] / image.height)
        image = image.resize((int(image.width * scale), int(image.height * scale)), Image.Resampling.LANCZOS)
        left = abs(self.render_size[0] - image.width) // 2
        top = abs(self.render_size[1] - image.height) // 2
        right = left + self.render_size[0]
        bottom = top + self.render_size[1]
        if left >= right or top >= bottom:
            return None
        image = image.crop((left, top, right, bottom))
        output = BytesIO()
        image.save(output, format='PNG')
        output.seek(0)
        return output

    def provide(self):
        image_url = self.request_image()
        if image_url is None:
            return None
        image_data = self.download_image(image_url)
        if image_data is None:
            return None
        image_data = self.crop(image_data)
        if image_data is None:
            return None
        return self.create_image(image_data, image_url)