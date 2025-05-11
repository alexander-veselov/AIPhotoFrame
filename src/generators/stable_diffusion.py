import requests
import base64
from io import BytesIO
from utils import calculate_generate_size
    
class StableDiffusion:
    DEFAULT_PROMPT = "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, "
    DEFAULT_NEGATIVE_PROMPT = "score_6, score_5, score_4, bad anatomy, "
    HIGHRES_SCALE = 1.5

    def __init__(self, ip, port):
        self.txt2img_url = 'http://{0}:{1}/sdapi/v1/txt2img'.format(ip, port)
        self.png_info_url = 'http://{0}:{1}/sdapi/v1/png-info'.format(ip, port)

    def post_txt2img(self, size, prompt, negative_prompt):
        width, height = calculate_generate_size(size)
        params = {
            "prompt": StableDiffusion.DEFAULT_PROMPT + prompt,
            "negative_prompt": StableDiffusion.DEFAULT_NEGATIVE_PROMPT + negative_prompt,
            "seed": -1,
            "steps": 20,
            "cfg_scale": 7,
            "width": width,
            "height": height,
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
        
        return requests.post(self.txt2img_url, json=params)

    def post_png_info(self, image_data):
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        return requests.post(self.png_info_url, json={"image": image_base64})

    def generate(self, size, prompt, negative_prompt=""):
        txt2img_response = self.post_txt2img(size, prompt, negative_prompt)
        if txt2img_response.status_code != 200:
            print("txt2img response error: {0}".format(txt2img_response.status_code))
            return None

        image_data = base64.b64decode(txt2img_response.json()["images"][0])
    
        generation_info = ""
        png_info_response = self.post_png_info(image_data)
        if png_info_response.status_code == 200:
            generation_info = png_info_response.json()["info"]
        else:
            print("png_info response error: {0}".format(png_info_response.status_code))

        return BytesIO(image_data), generation_info
