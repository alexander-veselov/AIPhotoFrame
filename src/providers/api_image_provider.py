import time
import requests
from io import BytesIO
from urllib.parse import urljoin
from providers.image_provider import ImageProvider

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

    def get_json(self, endpoint: str, params: dict = None):
        url = self._build_url(endpoint)

        try:
            response = requests.get(
                url,
                params=params or {},
                timeout=self.timeout
            )

            if response.status_code != 200:
                print(f"API error {response.status_code} for {response.url}")
                return None

            return response.json()

        except Exception as e:
            print(f"API request failed: {e}")
            return None

    def get_bytes(self, url: str):
        try:
            response = requests.get(url, timeout=self.timeout)

            if response.status_code != 200:
                print(f"Image download error {response.status_code}")
                return None

            return BytesIO(response.content)

        except Exception as e:
            print(f"Download failed: {e}")
            return None

    def request_image_url(self):
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

        image_url = self.request_image_url()

        if not image_url:
            self._on_failure()
            return None

        image_data = self.get_bytes(image_url)

        if not image_data:
            self._on_failure()
            return None

        self.failure_count = 0
        self.next_retry_time = 0

        return self.create_image(image_data, image_url)