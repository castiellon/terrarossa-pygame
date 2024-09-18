import pygame
from globals import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, position, image: pygame.Surface):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = position)