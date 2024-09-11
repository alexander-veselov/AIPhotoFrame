import requests
import base64
from io import BytesIO

def calculate_generate_size(screen_size, minimum_longest_size = 1024):
    minimum_longest_size = max(minimum_longest_size, max(screen_size))
    screen_width, screen_height = screen_size
    horizontal = screen_width > screen_height
    if horizontal:
        ratio = minimum_longest_size // screen_width
        return (minimum_longest_size, screen_height * ratio)
    else:
        ratio = minimum_longest_size // screen_height
        return (screen_width * ratio, minimum_longest_size)
    
class StableDiffusion:
    DEFAULT_PROMPT = "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, "
    DEFAULT_NEGATIVE_PROMPT = "score_6, score_5, score_4, bad anatomy, "

    def __init__(self, ip, port, highres_scale=2):
        self.url = 'http://{0}:{1}/sdapi/v1/txt2img'.format(ip, port)
        # TODO: make highres_scale as program input parameter
        self.highres_scale = highres_scale

    def generate(self, size, prompt, negative_prompt=""):
        width, height = calculate_generate_size(size)
        params = {
            "prompt": StableDiffusion.DEFAULT_PROMPT + prompt,
            "negative_prompt": StableDiffusion.DEFAULT_NEGATIVE_PROMPT + negative_prompt,
            "seed": -1,
            "steps": 20,
            "cfg_scale": 7,
            "width": width // self.highres_scale,
            "height": height // self.highres_scale,
            "sampler_name": "DPM++ 2M",
            "scheduler": "Karras",
        }
        
        if self.highres_scale > 1:
            params.update({
                "enable_hr": True,
                "hr_scale": self.highres_scale,
                "hr_upscaler": "Latent",
                "denoising_strength": 0.7
            })

        response = requests.post(self.url, json=params)
        if response.status_code != 200:
            print("response error: {0}".format(response.status_code))
            return None

        response_json = response.json()
        image_data = base64.b64decode(response_json["images"][0])
        return BytesIO(image_data)
