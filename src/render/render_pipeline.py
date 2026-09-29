from generated_image import GeneratedImage
from render.render_config import RenderConfig
from render.render_stage import RenderStage
from render.stages.dashboard_stage import DashboardStage
from render.stages.flip_and_rotate_stage import FlipAndRotateStage
from render.stages.calibrate_stage import CalibrateStage

class RenderPipeline:
    def __init__(self, render_config: RenderConfig):
        self.stages = []
        self.render_config = render_config
        self.add_stage(DashboardStage(render_config))
        self.add_stage(CalibrateStage(render_config))
        self.add_stage(FlipAndRotateStage(render_config))

    def add_stage(self, stage: RenderStage):
        self.stages.append(stage)

    def process(self, image: GeneratedImage) -> GeneratedImage:
        for stage in self.stages:
            image = stage.process(image)
        return image