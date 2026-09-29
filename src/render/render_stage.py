from generated_image import GeneratedImage
from render.render_config import RenderConfig

class RenderStage:
    def __init__(self, render_config: RenderConfig):
        self.render_config = render_config

    def process(self, image: GeneratedImage) -> GeneratedImage:
        raise NotImplementedError()