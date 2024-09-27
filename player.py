import pygame
from globals import *
from events import EventHandler
from texturedata import *
from sounds import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, image: pygame.Surface, parameters: dict, position = (200, 0)) -> None:
        super().__init__(groups)
        self.game_over = False
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        self.textures = gen_textures()
        #parameters section
        self.group_list = parameters["group_list"]
        self.block_group = self.group_list["block_group"]
        self.mob_group = self.group_list["mob_group"]
        self.inventory = parameters["inventory"]

        #health params
        self.health = parameters["health"]

        self.velocity = pygame.math.Vector2()
        self.mass = MASS
        self.terminal_velocity = TERMINALVELOCITY*MASS

        #is grounded??
        self.grounded = True

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.velocity.x = -VELOCITY_X
        if keys[pygame.K_d]:
            self.velocity.x = VELOCITY_X
        if self.velocity.x > 0:
            self.velocity.x -= 0.4
        if self.velocity.x < 0:
            self.velocity.x += 0.4
        if abs(self.velocity.x) < 0.5:
            self.velocity.x = 0
        #jumping
        if self.grounded and EventHandler.keydown(pygame.K_w):
            self.velocity.y = VELOCITY_Y
            AUDIO["jump"].play()


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

    def block_handling(self):
        placed = False
        collision = False
        mouse_pos= self.get_adjusted_mouse_position()


        if EventHandler.clicked_any():
            for block in self.block_group:
                if block.rect.collidepoint(mouse_pos):
                    collision = True
                    if EventHandler.clicked(1): #breking the block
                        if block.name != "default":
                            self.inventory.add_item(block)
                            AUDIO[block.name].play()
                        block.kill()
                if EventHandler.clicked(3):
                    if not collision:
                        placed = True
        if placed and not collision:
            self.inventory.use(player = self, pos = self.get_block_pos(mouse_pos), mob_group = self.mob_group)

    def get_adjusted_mouse_position(self) -> tuple:
        mouse_position = pygame.mouse.get_pos()

        player_offset = pygame.math.Vector2()
        player_offset.x = SCREENWIDTH/2 - self.rect.centerx
        player_offset.y = SCREENHEIGHT/2 - self.rect.centery

        return (mouse_position[0] - player_offset.x, mouse_position[1] - player_offset.y)

    def get_block_pos(self, mouse_pos: tuple):
        return(int((mouse_pos[0]//TILESIZE)*TILESIZE), int((mouse_pos[1]//TILESIZE)*TILESIZE))




    def update(self):
        self.input()
        self.do_texture()
        self.move()
        self.block_handling()
        print(self.rect.x//TILESIZE)
        
        if self.health <= 0 or self.rect.y > SCREENHEIGHT*3:
            self.kill()
            self.game_over = True

