import logging
import time
import json
import requests
from io import BytesIO
from urllib.parse import urljoin
from providers.image_provider import ImageProvider

class ImageResult:
    def __init__(self, url: str, source: str = None):
        self.url = url
        self.source = source

class ApiImageProvider(ImageProvider):
    def __init__(self, width, height, rotate, base_url: str, timeout=10):
        super().__init__(width, height, rotate)
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.failure_count = 0
        self.next_retry_time = 0
        self.faulty = False

    def _build_url(self, endpoint: str) -> str:
        return urljoin(self.base_url + "/", endpoint.lstrip("/"))
    
    def _request(self, url: str, params: dict = None):
        headers = {
            "User-Agent": "curl/8.0",
            "Accept": "application/json"
        }
        return requests.get(
            url,
            params=params or {},
            timeout=self.timeout,
            headers=headers
        )

    def get_json(self, endpoint: str, params: dict = None):
        url = self._build_url(endpoint)

        try:
            response = self._request(url, params)

            if response.status_code != 200:
                logging.error(f"API error {response.status_code} for {response.url}")
                return None

            return response.json()

        except Exception as e:
            logging.error(f"API request failed: {e}")
            return None

    def get_bytes(self, url: str):
        try:
            response = self._request(url)

            if response.status_code != 200:
                logging.error(f"Image download error {response.status_code}")
                return None

            return BytesIO(response.content)

        except Exception as e:
            logging.error(f"Download failed: {e}")
            return None

    def request_image(self):
        raise NotImplementedError()

    def _on_failure(self):
        self.failure_count += 1

        delay = min(300, 2 ** self.failure_count)

        self.next_retry_time = time.time() + delay

        if delay >= 300:
            self.faulty = True

    def provide(self):
        if self.faulty:
            return None

        if time.time() < self.next_retry_time:
            return None

        result = self.request_image()

        if not result:
            self._on_failure()
            return None

        image_data = self.get_bytes(result.url)

        if not image_data:
            self._on_failure()
            return None

        self.failure_count = 0
        self.next_retry_time = time.time() + 1.0

        image_info = json.dumps({
            "url": result.url,
            "source": result.source
        })

        image = self.create_image(image_data, image_info)

        return image