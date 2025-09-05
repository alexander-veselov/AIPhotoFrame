import time
import queue
import threading
from providers.image_provider import ImageProvider

class ConcurrentImageProvider(ImageProvider):
    def __init__(self, width, height, rotate, flip):
        super().__init__(width, height, rotate, flip)
        self.queue = queue.Queue(maxsize=3)
        self.running = False
        self.thread = None

    def provide(self):
        if not self.running:
            self.start()
        try:
            return self.queue.get_nowait()
        except queue.Empty:
            return None
        
    def start(self):
        if not self.thread or not self.thread.is_alive():
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

    def _run(self):
        self.running = True
        while self.running:
            if not self.queue.full():
                image = self.concurrent_provide()
                if image is not None:
                    self.queue.put(image)
            time.sleep(0.5)

    def concurrent_provide(self):
        raise NotImplementedError()