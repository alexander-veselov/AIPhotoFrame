import pygame
import requests
import argparse
import sys
import base64
from io import BytesIO


def generate_image(port, width, height):
    url = 'http://127.0.0.1:{0}/sdapi/v1/txt2img'.format(port)
    myobj = {
        "prompt": "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, 1girl",
        "negative_prompt": "score_6, score_5, score_4, bad anatomy, nsfw, naked",
        "seed": -1,
        "steps": 40,
        "cfg_scale": 7,
        "width": width,
        "height": height,
        "hr_checkpoint_name": "hassakuXLHentai_v13",
        "hr_sampler_name": "DPM++ 2M",
        "hr_scheduler": "Karras",
    }

    response = requests.post(url, json=myobj)
    if response.status_code == 200:
        response_json = response.json()
        image_data = base64.b64decode(response_json["images"][0])
        return BytesIO(image_data)
    else:
        print("response error: {0}".format(response.status_code))
        return None


def main(args):
    pygame.init()

    screen_size = (args.width, args.height)
    screen = pygame.display.set_mode(
        screen_size,
        pygame.FULLSCREEN if args.windowed else 0
    )

    pygame.mouse.set_visible(False)
    pygame.display.set_caption('AI Photo Frame')

    running = True
    while running:
        image_width = args.width * 2
        image_height = args.height * 2
        image_data = generate_image(args.port, image_width, image_height)
        image = pygame.image.load(image_data)
        scaled_image = pygame.transform.scale(image, screen_size)

        screen.blit(scaled_image, (0, 0))
        pygame.display.flip()

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
    parser.add_argument('--port', required=False, default=7861, type=int)
    args = parser.parse_args()
    sys.exit(main(args))
