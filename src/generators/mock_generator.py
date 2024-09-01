from io import BytesIO

class MockGenerator:
    def __init__(self):
        self.image_index = 0
        self.images = []
        for image_path in ["image1.bin", "image2.bin"]:
            with open("data/" + image_path, 'rb') as file:
                image_data = file.read()
                self.images.append(image_data)

    def generate(self, size, prompt, negative_prompt=""):
        self.image_index = (self.image_index + 1) % len(self.images)
        return BytesIO(self.images[self.image_index])