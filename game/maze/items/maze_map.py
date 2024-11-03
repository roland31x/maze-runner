from .item import Item
import pygame

class Maze_Map(Item):
    def __init__(self, x, y, config):
        texture = pygame.image.load('game/models/map.png').convert_alpha()
        super().__init__(x, y, texture, config)