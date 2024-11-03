from .item import Item
import pygame

class Key(Item):
    def __init__(self, x, y, config):
        texture = pygame.image.load('game/models/key.png').convert_alpha()
        super().__init__(x, y, texture, config)