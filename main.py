import pygame
import requests
import argparse
import sys
from io import BytesIO


def main(args):
    pygame.init()

    screen_size = (args.width, args.height)
    screen = pygame.display.set_mode(
        screen_size,
        pygame.FULLSCREEN if args.windowed else 0
    )

    pygame.mouse.set_visible(False)
    pygame.display.set_caption('AI Photo Frame')

    url = "https://wallpaperswide.com/download/famous_world_mountains-wallpaper-480x320.jpg"
    response = requests.get(url)
    image = pygame.image.load(BytesIO(response.content))
    image = pygame.transform.scale(image, screen_size)

    screen.blit(image, (0, 0))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='AI Photo Frame',
        description='Displays AI generated images in photo frame'
    )
    parser.add_argument('--windowed', action="store_false")
    parser.add_argument('--width', required=False, default=480, type=int)
    parser.add_argument('--height', required=False, default=320, type=int)
    args = parser.parse_args()
    sys.exit(main(args))
