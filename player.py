import pygame
from globals import *
from events import EventHandler
from texturedata import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, image: pygame.Surface, parameters: dict, position = (SCREENWIDTH // 2, SCREENHEIGHT // 2)) -> None:
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        self.textures = gen_textures()
        #parameters section
        self.block_group = parameters["block_group"]

        self.velocity = pygame.math.Vector2()
        self.mass = MASS
        self.terminal_velocity = TERMINALVELOCITY

        #is grounded??
        self.grounded = True

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.velocity.x = -VELOCITY_X
        if keys[pygame.K_d]:
            self.velocity.x = VELOCITY_X
        if not keys[pygame.K_a] and not keys[pygame.K_d] or keys[pygame.K_a] and keys[pygame.K_d]:
            self.velocity.x = 0
        #jumping
        if self.grounded and EventHandler.keydown(pygame.K_w):
            self.velocity.y = VELOCITY_Y


    def move(self):
        self.velocity.y += GRAVITY/MASS  # Apply gravity

        #terminal velocity check
        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

        self.rect.x += self.velocity.x
        self.check_collisions("horizontal")
        self.rect.y += self.velocity.y
        self.check_collisions("vertical")

    def check_collisions(self, direction):
        if direction == "horizontal":
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.x > 0: #moving right
                        self.rect.right = block.rect.left
                    if self.velocity.x < 0: #moving left
                        self.rect.left = block.rect.right
        elif direction == "vertical":
            collisions = 0  
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.y > 0: #moving down
                        self.rect.bottom = block.rect.top
                        collisions += 1
                    if self.velocity.y < 0: #moving up
                        self.rect.top = block.rect.bottom
            if collisions > 0:
                self.grounded = True
            else: 
                self.grounded = False
    def do_texture(self):
        if self.velocity.x > 0 and self.grounded:
            self.image = self.textures["player_run_right"]
        elif self.velocity.x < 0 and self.grounded:
            self.image =self.textures["player_run_left"]
        elif not self.grounded:
            self.image =self.textures["player_jump"]
        else:
            self.image = self.textures["player"]

    def update(self):
        self.input()
        self.do_texture()
        self.move()