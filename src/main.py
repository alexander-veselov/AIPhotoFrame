import sys
import argparse
from application import Application
from container import Container, override_display, override_image_provider, populate_dashboard_stages
from dependency_injector.wiring import Provide, inject
from validate import valid_ip, valid_port

@inject
def main(application: Application = Provide[Container.application]):
    return application.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='AI Photo Frame',
        description='Displays AI generated images in photo frame'
    )

    parser.add_argument('--display', type=str, default='pygame', choices=['pygame', 'ili9486', 'inky'], help='Display type.')
    parser.add_argument('--fps', type=int, default=5, help='Display framerate')
    parser.add_argument('--fullscreen', action='store_true')
    parser.add_argument('--rotate', action='store_true')
    parser.add_argument('--flip', action='store_true')
    parser.add_argument('--width', default=480, type=int)
    parser.add_argument('--height', default=320, type=int)

    parser.add_argument('--frame_duration', type=int, default=60, help='Frame display duration in seconds')
    parser.add_argument('--fade_duration', type=int, default=15, help='Fade transition duration in seconds')
    parser.add_argument('--dashboard', action='store_true')

    subparsers = parser.add_subparsers(dest='image_provider', required=True, help='Image provider type.')

    generate_parser = subparsers.add_parser('generate')
    generate_parser.add_argument('--ip', required=True, type=valid_ip, help='The IP address to connect to.')
    generate_parser.add_argument('--port', required=True, type=valid_port, help='The port number to connect to.')
    generate_parser.add_argument('--prompt', type=str, default='1girl, random', help='Positive prompt.')
    generate_parser.add_argument('--negative_prompt', type=str, default='nsfw, naked, nude', help='Negative prompt.')
    generate_parser.add_argument('--improve_prompt', action='store_true')

    mock_parser = subparsers.add_parser('mock')
    waifupics_parser = subparsers.add_parser('waifupics')

    args = parser.parse_args()

    container = Container()
    container.config.from_dict(vars(args))
    override_image_provider(container, args.image_provider)
    override_display(container, args.display)
    populate_dashboard_stages(container, args.dashboard)
    container.wire(modules=[__name__])

    sys.exit(main())