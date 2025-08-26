from io import BytesIO

class MockGenerator:
    def __init__(self):
        self.image_index = 0
        self.images = {"horizontal":[], "vertical": []}
        self._append("horizontal", "1.bin")
        self._append("horizontal", "2.bin")
        self._append("vertical", "1.bin")
        self._append("vertical", "2.bin")
    
    def _append(self, type, image_name):
        with open("data/" + type + "/" + image_name, 'rb') as file:
            image_data = file.read()
            self.images[type].append(image_data)

    def generate(self, size, prompt, negative_prompt=""):
        type = "horizontal" if size[0] > size[1] else "vertical"
        images = self.images[type]
        self.image_index = (self.image_index + 1) % len(images)
        return BytesIO(images[self.image_index]), ""