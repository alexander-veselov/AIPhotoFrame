from io import BytesIO
from providers.image_provider import ImageProvider

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