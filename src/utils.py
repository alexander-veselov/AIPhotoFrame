import os
import pygame
from PIL import Image, ImageChops, PngImagePlugin
from datetime import datetime

def surface_to_image(surface: pygame.Surface):
    pixel_data = pygame.image.tostring(surface, 'RGB')
    return Image.frombytes('RGB', surface.get_size(), pixel_data)

def save_image(surface: pygame.Surface, generation_info=""):
    image = surface_to_image(surface)
    save_dir = os.path.join(os.path.expanduser("~"), "Pictures/AIPhotoFrame")
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.png"
    file_path = os.path.join(save_dir, filename)
    meta = PngImagePlugin.PngInfo()
    meta.add_text("parameters", generation_info)
    image.save(file_path, pnginfo=meta)
    return file_path

def equal_images(image1, image2):
    diff = ImageChops.difference(image1, image2)
    return not bool(diff.getbbox())

def calculate_generate_size(screen_size, minimum_longest_size = 1216):
    minimum_longest_size = max(minimum_longest_size, max(screen_size))
    screen_width, screen_height = screen_size
    horizontal = screen_width > screen_height
    if horizontal:
        ratio = minimum_longest_size / screen_width
        return (minimum_longest_size, round(screen_height * ratio))
    else:
        ratio = minimum_longest_size / screen_height
        return (round(screen_width * ratio), minimum_longest_size)