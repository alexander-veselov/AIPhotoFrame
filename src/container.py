from dependency_injector import containers, providers

from application import Application
from generators.stable_diffusion import StableDiffusion
from generators.prompt_generator import PromptGenerator
from display.pygame_display import PygameDisplay
from providers.mock_image_provider import MockImageProvider
from providers.generated_image_provider import GeneratedImageProvider
from providers.waifupics_image_provider import WaifupicsImageProvider
from render.render import Renderer
from render.render_pipeline import RenderPipeline
from render.stages.dashboard_stage import DashboardStage
from render.stages.flip_and_rotate_stage import FlipAndRotateStage
from render.stages.calibrate_stage import CalibrateStage

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    display = providers.Singleton(
        PygameDisplay,
        width=config.width,
        height=config.height,
        fullscreen=config.fullscreen
    )

    renderer = providers.Singleton(
        Renderer,
        display=display,
        fps=config.fps,
        frame_duration=config.frame_duration,
        fade_duration=config.fade_duration
    )

    render_pipeline = providers.Singleton(
        RenderPipeline
    )

    image_generator = providers.Singleton(
        StableDiffusion,
        ip=config.ip,
        port=config.port
    )

    prompt_generator=providers.Singleton(
        PromptGenerator,
        ip=config.ip,
        port=config.port
    )

    image_provider = providers.Singleton(
        GeneratedImageProvider,
        image_generator=image_generator,
        prompt_generator=prompt_generator,
        prompt=config.prompt,
        negative_prompt=config.negative_prompt,
        width=config.width,
        height=config.height,
        rotate=config.rotate,
        improve_prompt=config.improve_prompt
    )

    application = providers.Singleton(
        Application,
        renderer=renderer,
        render_pipeline=render_pipeline,
        image_provider=image_provider
    )

def override_image_provider(container, image_provider):
    if image_provider == 'mock':
        container.override_providers(
            image_provider=providers.Singleton(
                    MockImageProvider,
                    width=container.config.width,
                    height=container.config.height,
                    rotate=container.config.rotate,
                )
            )
    elif image_provider == 'waifupics':
        container.override_providers(
            image_provider=providers.Singleton(
                WaifupicsImageProvider,
                    width=container.config.width,
                    height=container.config.height,
                    rotate=container.config.rotate,
                )
            )

def override_display(container, display):
    try:
        if display == 'ili9486':
            from display.ili9486_display import ILI9486Display
            container.override_providers(
                display=providers.Singleton(
                    ILI9486Display,
                    width=container.config.width,
                    height=container.config.height,
                )
            )
        if display == 'inky':
            from display.inky_display import InkyDisplay
            container.override_providers(
                display=providers.Singleton(
                    InkyDisplay,
                    width=container.config.width,
                    height=container.config.height
                )
            )
    except Exception as e:
        print(f'Failed to import {display} display: {e}')

def populate_dashboard_stages(container, dashboard):
    config = container.config
    render_pipeline = container.render_pipeline()
    if dashboard:
        render_pipeline.add_stage(DashboardStage())
    render_pipeline.add_stage(CalibrateStage(7, -35)) # TODO: make configurable
    render_pipeline.add_stage(FlipAndRotateStage(config.flip(), config.rotate()))
