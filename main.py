import pygame
import requests
import argparse
import sys
import base64
import os
from io import BytesIO


os.environ['DISPLAY'] = ':0'


def generate_image(ip, port, width, height):
    url = 'http://{0}:{1}/sdapi/v1/txt2img'.format(ip, port)
    params = {
        "prompt": "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, 1girl, random",
        "negative_prompt": "score_6, score_5, score_4, bad anatomy, nsfw, naked",
        "seed": -1,
        "steps": 20,
        "cfg_scale": 7,
        "width": width,
        "height": height,
        "hr_checkpoint_name": "hassakuXLHentai_v13",
        "hr_sampler_name": "DPM++ 2M",
        "hr_scheduler": "Karras",
    }

    response = requests.post(url, json=params)
    if response.status_code == 200:
        response_json = response.json()
        image_data = base64.b64decode(response_json["images"][0])
        return BytesIO(image_data)
    else:
        print("response error: {0}".format(response.status_code))
        return None


def main(args):
    pygame.init()

    screen_size = (args.height, args.width) if args.rotate else (args.width, args.height)
    screen = pygame.display.set_mode(
        screen_size,
        pygame.FULLSCREEN if args.windowed else 0
    )

    pygame.mouse.set_visible(False)
    pygame.display.set_caption('AI Photo Frame')

    running = True
    while running:
        image_width = screen_size[0] * 2
        image_height = screen_size[1] * 2
        image_data = generate_image(args.ip, args.port, image_width, image_height)
        image = pygame.image.load(image_data)
        image = pygame.transform.smoothscale(image, screen_size)
        if args.rotate:
            image = pygame.transform.rotate(image, 90)
        if args.flip:
            image = pygame.transform.flip(image, flip_x=args.rotate, flip_y=not args.rotate)

        screen.blit(image, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONUP:
                running = False

    pygame.quit()
    return 0


def valid_ip(address):
    try:
        parts = address.split('.')
        if len(parts) != 4:
            raise ValueError
        for part in parts:
            if not 0 <= int(part) <= 255:
                raise ValueError
        return address
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid IP address: '{address}'")


def valid_port(port):
    port = int(port)
    if not (0 <= port <= 65535):
        raise argparse.ArgumentTypeError(f"Invalid port number: '{port}'")
    return port


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='AI Photo Frame',
        description='Displays AI generated images in photo frame'
    )
    parser.add_argument('--ip', type=valid_ip, required=True, help="The IP address to connect to.")
    parser.add_argument('--port', type=valid_port, required=True, help="The port number to connect to.")
    parser.add_argument('--windowed', action="store_false")
    parser.add_argument('--rotate', action="store_true")
    parser.add_argument('--flip', action="store_true")
    parser.add_argument('--width', required=False, default=480, type=int)
    parser.add_argument('--height', required=False, default=320, type=int)

    args = parser.parse_args()
    sys.exit(main(args))