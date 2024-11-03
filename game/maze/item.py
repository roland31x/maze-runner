class Item(object):
    def __init__(self, x, y, texture, radius):
        self.X = x
        self.Y = y
        self.texture = texture
        self.R = radius
        self.picked_up = False
        self.selected = False
        self.used = False

