import os
import pygame
from PIL import Image
from datetime import datetime

def surface_to_image(surface: pygame.Surface):
    pixel_data = pygame.image.tostring(surface, 'RGB')
    return Image.frombytes('RGB', surface.get_size(), pixel_data)

def save_image(surface: pygame.Surface):
    image = surface_to_image(surface)
    save_dir = os.path.join(os.path.expanduser("~"), "Pictures/AIPhotoFrame")
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.png"
    file_path = os.path.join(save_dir, filename)
    image.save(file_path)
    return file_path