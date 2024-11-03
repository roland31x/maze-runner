from .item import Item
import pygame

class Energy_Drink(Item):
    def __init__(self, x, y, radius):
        texture = pygame.image.load('game/models/can.png')
        super().__init__(x, y, texture, radius)