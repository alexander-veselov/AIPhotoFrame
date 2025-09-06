from generated_image import GeneratedImage

class RenderStage:
    def process(self, image: GeneratedImage) -> GeneratedImage:
        raise NotImplementedError()

class RenderPipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage: RenderStage):
        self.stages.append(stage)

    def process(self, image: GeneratedImage) -> GeneratedImage:
        for stage in self.stages:
            image = stage.process(image)
        return image