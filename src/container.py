from dependency_injector import containers, providers

from application import Application
from generators.stable_diffusion import StableDiffusion
from generators.prompt_generator import PromptGenerator
from display.pygame_display import PygameDisplay
from providers.mock_image_provider import MockImageProvider
from providers.generated_image_provider import GeneratedImageProvider
from providers.waifupics_image_provider import WaifupicsImageProvider
from render import Renderer

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
        flip=config.flip,
        improve_prompt=config.improve_prompt
    )

    application = providers.Singleton(
        Application,
        renderer=renderer,
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
                flip=container.config.flip)
            )
    elif image_provider == 'waifupics':
        container.override_providers(
            image_provider=providers.Singleton(
                WaifupicsImageProvider,
                width=container.config.width,
                height=container.config.height,
                rotate=container.config.rotate,
                flip=container.config.flip)
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
                    height=container.config.height,
                    skip_first_frame=True
                )
            )
    except Exception as e:
        print(f'Failed to import {display} display: {e}')