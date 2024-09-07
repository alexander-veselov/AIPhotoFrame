import pygame

class Display:
    def __init__(self):
        self.displays = []

    def get_surface(self):
        if len(self.displays) == 0:
            raise Exception("No displays provided")
        return self.displays[0].get_surface()

    def append(self, display):
        self.displays.append(display)

    def flip(self):
        for display in self.displays:
            display.flip()

    def reset(self):
        for display in self.displays:
            display.reset()

def create_surface(display, size, fullscreen):
    if "pygame" in display:
        return pygame.display.set_mode(
            size,
            pygame.DOUBLEBUF | (pygame.FULLSCREEN if fullscreen else 0)
        )
    else:
        return pygame.Surface(size)

def create_display(display_info, size, fullscreen):
    display = Display()
    surface = create_surface(display_info, size, fullscreen)
    for display_name in display_info.split('+'):
        try:
            if display_name == "ili9486":
                from display.ili9486_display import ILI9486Display
                display.append(ILI9486Display(surface))
            elif display_name == "pygame":
                from display.pygame_display import PygameDisplay
                display.append(PygameDisplay(surface))
            else:
                raise Exception("Unsupported display type")
        except Exception as e:
            print(f'Failed to create "{display_name}" display: {e}')
    return display