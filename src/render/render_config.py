class RenderConfig:
    def __init__(self, width, height, rotate, flip, width_shift, height_shift, dashboard):
        self.width = width
        self.height = height
        self.rotate = rotate
        self.flip = flip
        self.width_shift = width_shift
        self.height_shift = height_shift
        self.dashboard = dashboard
    
    def render_size(self):
        width = self.width - abs(self.width_shift)
        height = self.height - abs(self.height_shift)
        return (height, width) if self.rotate else (width, height)