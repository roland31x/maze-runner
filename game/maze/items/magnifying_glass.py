from .item import Item
import pygame

class Magnifying_Glass(Item):
    def __init__(self, x, y, config):
        texture = pygame.image.load('game/models/magnifying_glass.png').convert_alpha()
        super().__init__(x, y, texture, config)