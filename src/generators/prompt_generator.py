import requests
from utils import calculate_generate_size
    
class PromptGenerator:
    def __init__(self, ip, port):
        self.url = 'http://{0}:{1}/z-tipo/generate-prompt'.format(ip, port)

    def generate(self, size, prompt):
        width, height = calculate_generate_size(size)
        params = {
            "prompt": prompt,
            "aspect_ratio ": width / height,
            "temperature": 1.35,
            "top_p": 0.95,
            "top_k": 100,
            "tag_length": "long",
            "ban_tags": "chibi, background"
        }

        response = requests.post(self.url, json=params)
        if response.status_code != 200:
            print("response error: {0}".format(response.status_code))
            return None

        response_json = response.json()
        result = response_json["result"]
        prompt_parts = [part for part in result.split('\n') if part.strip()]

        # TODO: Improve API to support "tag only (DTG mode)"
        if len(prompt_parts) != 3:
            print(f'Unexpected number of prompt lines: {len(prompt_parts)}')
            return result
        
        special_tags, tags, natural_language = prompt_parts
        return special_tags + tags
