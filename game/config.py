class Config:
    def __init__(self) -> None:       
        self.default()

    def default(self):
        self.white = (255, 255, 255)
        self.black = (20, 20, 20)
        self.light_gray = (200,200,200)
        self.dark_gray = (59, 59, 82)
        ##############################
        self.sizeX = 16
        self.sizeY = 16
        self.player_speed = 8
        self.obj_radius = 45
        self.cellsize = 250
