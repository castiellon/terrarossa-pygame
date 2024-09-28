import pygame
import sys
from globals import *
from sprite import Entity, Mob
from player import Player
from texturedata import *
from opensimplex import OpenSimplex
from camera import Camera
from inventory import Inventory

class Scene:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.running = True
        self.played = False
        self.textures = gen_textures()
        self.background = pygame.image.load("res/background.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (SCREENWIDTH,SCREENHEIGHT))
        self.app.screen.blit(self.background, (0,0))
        self.sprites = Camera()
        self.blocks = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.group_list: dict[str, pygame.sprite.Group] = {
            "sprites":self.sprites,
            "block_group":self.blocks,
            "mob_group":self.mobs,
        }
        #inventory
        self.inventory = Inventory(self.app, self.textures)

        
        self.player = Player([self.sprites], image = self.textures["player"], parameters={"group_list":self.group_list,
                                                                                          "inventory":self.inventory,
                                                                                          "health": 3})

        #generation
        self.gen_world()
        self.create_mobs()

    def create_mobs(self):
        mob_positions = [(34*TILESIZE, 0)] #revert back!!! add more mobs(harder)
        for pos in mob_positions:
            Mob([self.sprites, self.mobs], pos, self.textures["zombie_static"], parameters={
                "block_group": self.blocks,
                "player": self.player,
                "damage": 1,
            })

    def gen_world(self):
        #grass biome
        noise_generator = OpenSimplex(seed = 15062002)
        heightmap = []
        for y in range(BIOMESIZE*3):
            noise_value = noise_generator.noise2(y * 0.1, 0)
            height = int((noise_value + 1) * 8 + 3)
            heightmap.append(height)
        
        smooth_heightmap = []
        smoothing_window = 6  # Adjust the window size for smoothing
        for i in range(len(heightmap)):
            window_values = heightmap[max(0, i-smoothing_window):min(len(heightmap), i+smoothing_window+1)]
            smooth_height = sum(window_values) // len(window_values)
            smooth_heightmap.append(smooth_height)

        for x in range(0,BIOMESIZE):
            for y in range(smooth_heightmap[x]):
                y_offset = 5-y
                block_type = "dirt"
                if y == smooth_heightmap[x]-1:
                    block_type ="grass"
                if y < smooth_heightmap[x]-4:
                    block_type = "stone"

                # Calculate alpha value based on the height
                alpha_value = int(255 * (y / smooth_heightmap[x]))
                surface = self.textures[block_type].copy()
                surface.set_alpha(alpha_value)  # Set alpha based on height

                Entity([self.sprites, self.blocks], (x*TILESIZE,y_offset*TILESIZE), surface, name = block_type)
        #corrupt biome
        for x in range(BIOMESIZE, 2*BIOMESIZE):
            for y in range(smooth_heightmap[x]):
                y_offset = 5-y
                block_type = "dirt"
                if y == smooth_heightmap[x]-1:
                    block_type ="corrupt_grass"
                if y < smooth_heightmap[x]-4:
                    block_type = "stone"

                alpha_value = int(255 * (y / smooth_heightmap[x]))
                surface = self.textures[block_type].copy()
                surface.set_alpha(alpha_value)  # Set alpha based on height

                Entity([self.sprites, self.blocks], (x*TILESIZE,y_offset*TILESIZE), surface, name = block_type)
        #crimson biome
        for x in range(2*BIOMESIZE, len(smooth_heightmap)):
            for y in range(smooth_heightmap[x]):
                y_offset = 5-y
                block_type = "dirt"
                if y == smooth_heightmap[x]-1:
                    block_type ="crimson_grass"
                if y < smooth_heightmap[x]-4:
                    block_type = "stone"

                alpha_value = int(255 * (y / smooth_heightmap[x]))
                surface = self.textures[block_type].copy()
                surface.set_alpha(alpha_value)  # Set alpha based on height

                Entity([self.sprites, self.blocks], (x*TILESIZE,y_offset*TILESIZE), surface, name = block_type)

    def is_game_over(self):
        if self.player.game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over!!", True, "white")

            text_2 = font.render("stay determined", True, "white")

            self.app.screen.blit(text,(SCREENWIDTH // 2 - text.get_width() // 2, 200))
            self.app.screen.blit(text_2,(SCREENWIDTH // 2 - text_2.get_width() // 2, 300))
            if not self.played:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("res/lightless.mp3")
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(1)
                self.played = True
            if not pygame.mixer.music.get_busy():
                self.running = False   

    def update(self):
        self.inventory.update()
        self.sprites.update()
    def draw(self):
        if self.player.velocity != pygame.math.Vector2():
            self.screen.blit(self.background, (0,0))

        self.is_game_over()
        self.sprites.draw(self.player, self.screen)
        self.inventory.draw()
        for mob in self.mobs:
            mob.draw(self.screen)