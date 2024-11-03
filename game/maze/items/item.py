from ...player import ConfigObjectDrawable

class Item(ConfigObjectDrawable):
    def __init__(self, x, y, texture, config):
        super().__init__(config)
        self.X = x
        self.Y = y
        self.texture = texture
        self.picked_up = False
        self.selected = False
        self.used = False
        self.is_in_use = False

