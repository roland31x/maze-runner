from .item import Item
import pygame

class Key(Item):
    def __init__(self, x, y, radius):
        texture = pygame.image.load('game/models/key.png')
        super().__init__(x, y, texture, radius)