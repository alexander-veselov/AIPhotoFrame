import os
import sys
import argparse
from application import Application
from utils import valid_ip, valid_port

def main(args):
    os.environ['DISPLAY'] = ':0'
    application = Application(args)
    return application.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='AI Photo Frame',
        description='Displays AI generated images in photo frame'
    )
    parser.add_argument('--ip', type=valid_ip, required=True, help="The IP address to connect to.")
    parser.add_argument('--port', type=valid_port, required=True, help="The port number to connect to.")
    parser.add_argument('--prompt', type=str, required=False, default="1girl, random", help="Positive prompt.")
    parser.add_argument('--negative_prompt', type=str, required=False, default="nsfw, naked, nude", help="Negative prompt.")
    parser.add_argument('--fps', type=int, required=False, default=15, help="Display framerate")
    parser.add_argument('--frame_duration', type=int, required=False, default=60, help="Frame display duration in seconds")
    parser.add_argument('--fade_duration', type=int, required=False, default=15, help="Fade transition duration in seconds")
    parser.add_argument('--windowed', action="store_false")
    parser.add_argument('--rotate', action="store_true")
    parser.add_argument('--flip', action="store_true")
    parser.add_argument('--width', required=False, default=480, type=int)
    parser.add_argument('--height', required=False, default=320, type=int)

    args = parser.parse_args()
    sys.exit(main(args))
