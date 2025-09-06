from utils import equal_images

class ImageObserver:
    def __init__(self, image=None):
        self.image = image
    
    def update(self, image):
        if self.image is None:
            self.image = image
            return True
        equal = equal_images(self.image, image)
        if not equal:
            self.image = image
        return not equal