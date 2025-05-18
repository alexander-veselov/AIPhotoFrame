import requests
from utils import calculate_generate_size
    
class PromptGenerator:
    def __init__(self, ip, port):
        self.url = 'http://{0}:{1}/z-tipo/generate-prompt'.format(ip, port)

    def process(self, size, prompt, negative_prompt, improve_prompt):
        DEFAULT_PROMPT = "score_9, score_8_up, score_7_up, "
        DEFAULT_NEGATIVE_PROMPT = "score_6, score_5, score_4, bad anatomy, "
        prompt = DEFAULT_PROMPT + prompt
        negative_prompt = DEFAULT_NEGATIVE_PROMPT + negative_prompt
        if improve_prompt:
            prompt = self._generate(size, prompt)
        return prompt, negative_prompt

    def _generate(self, size, prompt):
        width, height = calculate_generate_size(size)
        params = {
            "prompt": prompt,
            "aspect_ratio ": width / height,
            "temperature": 1.35,
            "top_p": 0.95,
            "top_k": 100,
            "tag_length": "long",
            "ban_tags": "chibi, loli, simple background, background, border, multiple views, animal, monochrome",
            "format_select": "tag only (DTG mode)"
        }

        response = requests.post(self.url, json=params)
        if response.status_code != 200:
            print("response error: {0}".format(response.status_code))
            return None

        response_json = response.json()
        return response_json["result"]