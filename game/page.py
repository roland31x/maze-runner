class Page(object):
    def __init__(self, engine):
        self.engine = engine
        self.pygame = engine.pygame
        self.screen = engine.screen
        self.clock = engine.clock
    def render(self):
        pass
    def handle_event(self, event):
        pass