import pygame

from .drawable import ConfigObjectDrawable

class Player(ConfigObjectDrawable):
    def __init__(self, name, speed, config):
        super().__init__(config)
        self.name = name
        self.color = (255, 0, 0)
        self.X = 1
        self.Y = 1
        self.speed = speed
        self.last_dir = 2
        self.moving = False
        self.sprites = [
            [
                pygame.image.load('game/models/2_0.png'),
                pygame.image.load('game/models/2_1.png'),
                pygame.image.load('game/models/2_0.png'),
                pygame.image.load('game/models/2_3.png'),
            ],
            [
                pygame.image.load('game/models/1_0.png'),
                pygame.image.load('game/models/1_1.png'),
                pygame.image.load('game/models/1_0.png'),
                pygame.image.load('game/models/1_3.png'),
            ],
            [
                pygame.image.load('game/models/0_0.png'),
                pygame.image.load('game/models/0_1.png'),
                pygame.image.load('game/models/0_0.png'),
                pygame.image.load('game/models/0_3.png'),
            ],
            [
                pygame.image.load('game/models/3_0.png'),
                pygame.image.load('game/models/3_1.png'),
                pygame.image.load('game/models/3_0.png'),
                pygame.image.load('game/models/3_3.png'),
            ]
        ]

    def move(self, dir, lastdir):
        self.X += dir[0] * self.speed
        self.Y += dir[1] * self.speed
        self.last_dir = lastdir

class Target(ConfigObjectDrawable):
    def __init__(self, X, Y, config):
        super().__init__(config)
        self.X = X
        self.Y = Y
        self.open = 1
        self.sprites = [ 
            pygame.image.load('game/models/trapdoor_closed.png'),
            pygame.image.load('game/models/trapdoor.png')
        ]
