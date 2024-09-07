from dependency_injector import containers, providers

from application import Application
from generators.mock_generator import MockGenerator
from generators.stable_diffusion import StableDiffusion
from display.pygame_display import PygameDisplay
from image_provider import ImageProvider
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

    image_provider = providers.Singleton(
        ImageProvider,
        generator=image_generator,
        renderer=renderer,
        prompt=config.prompt,
        negative_prompt=config.negative_prompt,
        width=config.width,
        height=config.height,
        rotate=config.rotate,
        flip=config.flip
    )

    application = providers.Singleton(
        Application,
        renderer=renderer,
        image_provider=image_provider
    )

def override_generator(container, generator):
    if generator == 'mock_generator':
        container.override_providers(
            image_generator=providers.Singleton(MockGenerator)
        )

def override_display(container, display):
    if display == 'ili9486':
        try:
            from display.ili9486_display import ILI9486Display
            container.override_providers(
                display=providers.Singleton(ILI9486Display, container.surface)
            )
        except Exception as e:
            print(f'Failed to import ILI9486Display: {e}')