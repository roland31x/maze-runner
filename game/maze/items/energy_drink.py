from .item import Item
import pygame

class Energy_Drink(Item):
    def __init__(self, x, y, config):
        texture = pygame.image.load('game/models/can.png').convert_alpha()
        super().__init__(x, y, texture, config)