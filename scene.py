import pygame
from globals import *
from sprite import Entity
from player import Player
from texturedata import *
from opensimplex import OpenSimplex

class Scene:
    def __init__(self, app):
        self.app = app

        self.textures = gen_textures()
        self.sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.gen_world()

        
        self.player = Player([self.sprites], image = self.textures["player"], parameters={'block_group':self.blocks})


    def gen_world(self):
        noise_generator = OpenSimplex(seed = 1506)
        heightmap = []
        for y in range(20):
            noise_value = noise_generator.noise2(y * 4, 0)
            height = int((noise_value + 1) * 1 + 4)
            heightmap.append(height)
        for x in range(len(heightmap)):
            for y in range(heightmap[x]):
                y_offset = 5-y+6
                texture = self.textures["dirt"]
                if y == heightmap[x]-1:
                    texture = self.textures["grass"]
                if y < heightmap[x]-3:
                    texture = self.textures["stone"]
                Entity([self.sprites, self.blocks], (x*TILESIZE,y_offset*TILESIZE), texture)


    def update(self):
        self.sprites.update()
    def draw(self):
        self.app.screen.fill("lightblue")
        self.sprites.draw(self.app.screen)