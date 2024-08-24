import requests
import base64
from io import BytesIO

def calculate_generate_size(screen_size, target_longest_size = 1024):
    screen_width, screen_height = screen_size
    horizontal = screen_width > screen_height
    if horizontal:
        ratio = target_longest_size // screen_width
        return (target_longest_size, screen_height * ratio)
    else:
        ratio = target_longest_size // screen_height
        return (screen_width * ratio, target_longest_size)
    
class StableDiffusion:
    DEFAULT_PROMPT = "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, "
    DEFAULT_NEGATIVE_PROMPT = "score_6, score_5, score_4, bad anatomy, "

    def __init__(self, ip, port, screen_size):
        self.url = 'http://{0}:{1}/sdapi/v1/txt2img'.format(ip, port)
        self.width, self.height = calculate_generate_size(screen_size)

    def generate(self, prompt, negative_prompt=""):
        params = {
            "prompt": StableDiffusion.DEFAULT_PROMPT + prompt,
            "negative_prompt": StableDiffusion.DEFAULT_NEGATIVE_PROMPT + negative_prompt,
            "seed": -1,
            "steps": 20,
            "cfg_scale": 7,
            "width": self.width,
            "height": self.height,
            "sampler_name": "DPM++ 2M",
            "scheduler": "Karras",
        }

        response = requests.post(self.url, json=params)
        if response.status_code != 200:
            print("response error: {0}".format(response.status_code))
            return None

        response_json = response.json()
        image_data = base64.b64decode(response_json["images"][0])
        return BytesIO(image_data)
