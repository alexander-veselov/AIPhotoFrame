from utils import save_image, surface_to_image
from image_observer import ImageObserver
from generated_image import GeneratedImage

class ImageSaver:
    def __init__(self, transform):
        self.transform = transform
        self.image_observer = ImageObserver()
    
    def save_image(self, image: GeneratedImage):
        if image is not None:
            if self.image_observer.update(surface_to_image(image)):
                transformed_image = self.transform(image)
                image_path = save_image(transformed_image, image.generation_info)
                print(f'Image saved to {image_path}')