from generated_image import GeneratedImage
from render.render_stage import RenderStage
from render.stages.dashboard_stage import DashboardStage
from render.stages.flip_and_rotate_stage import FlipAndRotateStage
from render.stages.calibrate_stage import CalibrateStage

class RenderPipeline:
    def __init__(self):
        self.stages = []

    @staticmethod
    def from_config(config):
        render_pipeline = RenderPipeline()
        if config['dashboard']:
            render_pipeline.add_stage(DashboardStage())
        render_pipeline.add_stage(CalibrateStage(config['shift_x'], config['shift_y']))
        render_pipeline.add_stage(FlipAndRotateStage(config['flip'], config['rotate']))
        return render_pipeline

    def add_stage(self, stage: RenderStage):
        self.stages.append(stage)

    def process(self, image: GeneratedImage) -> GeneratedImage:
        for stage in self.stages:
            image = stage.process(image)
        return image