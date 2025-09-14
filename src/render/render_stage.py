from generated_image import GeneratedImage

class RenderStage:
    def process(self, image: GeneratedImage) -> GeneratedImage:
        raise NotImplementedError()