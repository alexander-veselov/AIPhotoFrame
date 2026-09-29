class RenderConfig:
    def __init__(self, width, height, rotate, flip, shift_x, shift_y):
        self.width = width
        self.height = height
        self.rotate = rotate
        self.flip = flip
        self.shift_x = shift_x
        self.shift_y = shift_y
    
    def render_size(self):
        width = self.width - abs(self.shift_x)
        height = self.height - abs(self.shift_y)
        return (height, width) if self.rotate else (width, height)