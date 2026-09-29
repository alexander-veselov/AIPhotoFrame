import logging
from dependency_injector import containers, providers

from application import Application
from generators.stable_diffusion import StableDiffusion
from generators.prompt_generator import PromptGenerator
from display.pygame_display import PygameDisplay
from providers.mock_image_provider import MockImageProvider
from providers.generated_image_provider import GeneratedImageProvider
from providers.waifupics_image_provider import WaifupicsImageProvider
from providers.waifuim_image_provider import WaifuimImageProvider
from providers.nekosbest_image_provider import NekosBestImageProvider
from providers.danbooru_image_provider import DanbooruImageProvider
from providers.combined_image_provider import CombinedImageProvider
from render.render import Renderer
from render.render_config import RenderConfig

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    display = providers.Singleton(
        PygameDisplay,
        width=config.width,
        height=config.height,
        fullscreen=config.fullscreen
    )

    render_config = providers.Singleton(
        RenderConfig,
        width=config.width,
        height=config.height,
        rotate=config.rotate,
        flip=config.flip,
        width_shift=config.width_shift,
        height_shift=config.height_shift,
        dashboard=config.dashboard
    )

    renderer = providers.Singleton(
        Renderer,
        display=display,
        fps=config.fps,
        frame_duration=config.frame_duration,
        fade_duration=config.fade_duration
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
        render_config=render_config,
        image_generator=image_generator,
        prompt_generator=prompt_generator,
        prompt=config.prompt,
        negative_prompt=config.negative_prompt,
        improve_prompt=config.improve_prompt
    )

    application = providers.Singleton(
        Application,
        render_config=render_config,
        renderer=renderer,
        image_provider=image_provider
    )

def override_image_provider(container, image_provider, provider_names=None):
    if image_provider == 'mock':
        container.override_providers(
            image_provider=providers.Singleton(
                MockImageProvider,
                render_config=container.render_config()
            )
        )
    elif image_provider == 'providers':
        IMAGE_PROVIDERS = {
            'waifupics': WaifupicsImageProvider,
            'nekosbest': NekosBestImageProvider,
            'waifuim': WaifuimImageProvider,
            'danbooru': DanbooruImageProvider,
        }

        combined = CombinedImageProvider(
            render_config=container.render_config()
        )

        for name in provider_names:
            combined.add_provider(IMAGE_PROVIDERS[name])

        container.override_providers(
            image_provider=providers.Object(combined)
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
        logging.error(f'Failed to import {display} display: {e}')
