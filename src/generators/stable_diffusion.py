import requests
import base64
from io import BytesIO
from utils import calculate_generate_size
    
class StableDiffusion:
    DEFAULT_PROMPT = "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, "
    DEFAULT_NEGATIVE_PROMPT = "score_6, score_5, score_4, bad anatomy, "
    HIGHRES_SCALE = 2

    def __init__(self, ip, port):
        self.url = 'http://{0}:{1}/sdapi/v1/txt2img'.format(ip, port)

    def generate(self, size, prompt, negative_prompt=""):
        width, height = calculate_generate_size(size)
        params = {
            "prompt": StableDiffusion.DEFAULT_PROMPT + prompt,
            "negative_prompt": StableDiffusion.DEFAULT_NEGATIVE_PROMPT + negative_prompt,
            "seed": -1,
            "steps": 20,
            "cfg_scale": 7,
            "width": width // StableDiffusion.HIGHRES_SCALE,
            "height": height // StableDiffusion.HIGHRES_SCALE,
            "sampler_name": "DPM++ 2M",
            "scheduler": "Karras",
        }
        
        if StableDiffusion.HIGHRES_SCALE > 1:
            params.update({
                "enable_hr": True,
                "hr_scale": StableDiffusion.HIGHRES_SCALE,
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
