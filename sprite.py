import pygame
from globals import *
import math
from random import choice
from sounds import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, position, image: pygame.Surface, name: str = "default"):
        super().__init__(groups)
        self.image = image
        self.name = name
        self.in_groups = groups
        self.rect = self.image.get_rect(topleft = position)
        

class Mob(Entity):
    def __init__(self, groups, position, image: pygame.Surface, parameters = {}):
        super().__init__(groups, position, image)

        if parameters:
            self.block_group = parameters["block_group"]
            self.player = parameters["player"]
            self.damage = parameters["damage"]

        self.velocity = pygame.math.Vector2()
        self.max_health = 20
        self.health = 20
        self.mass = 20
        self.speed = 1
        self.terminal_velocity = TERMINALVELOCITY*MASS
        #states
        self.attacking = True
        self.attacked = False
        self.grounded = False
        #cooldowns
        self.attack_cooldown = 60
        self.counter = self.attack_cooldown
        #health bar settings
        self.health_bar_length = 40
        self.health_bar_height = 5
    def get_distance(self):
        return abs(math.sqrt((self.rect.x - self.player.rect.x)**2 + (self.rect.y - self.player.rect.y)**2))
    
    def move(self):
        self.velocity.y += GRAVITY/self.mass  # Apply gravity

        #terminal velocity check
        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

        #distance calculation
        if self.get_distance() < TILESIZE*16:
            #within range
            self.attacking = True
            #run to the player
            if self.rect.x > self.player.rect.x:
                self.velocity.x = -self.speed
            elif self.rect.x < self.player.rect.x:
                self.velocity.x = self.speed
        else: 
            self.attacking = False
            self.velocity.x = 0

        self.rect.x += self.velocity.x #apply horizontal velocity
        self.check_collisions("horizontal")
        self.rect.y += self.velocity.y
        self.check_collisions("vertical")

        # jump when stuck
        if self.grounded and self.attacking and abs(self.velocity.x) < 0.1:
            self.velocity.y = -12

    def check_collisions(self, direction):
        if direction == "horizontal":
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.x > 0: #moving right
                        self.rect.right = block.rect.left
                    if self.velocity.x < 0: #moving left
                        self.rect.left = block.rect.right
                    self.velocity.x = 0
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

    def check_player_collision(self):
        if self.attacking and not self.attacked:
            if self.rect.colliderect(self.player.rect):
                self.player.health -= self.damage
                self.zombie_sounds = ["zombie_1","zombie_2"]
                AUDIO[choice(self.zombie_sounds)].play()
                self.attacked = True

                if self.player.rect.centerx > self.rect.centerx:
                    self.player.velocity.x = 10
                elif self.player.rect.centerx < self.rect.centerx:
                    self.player.velocity.x = -10

    def draw(self,screen):
        # Create health bars
        offset = pygame.math.Vector2()
        offset.x = SCREENWIDTH / 2 - self.player.rect.centerx
        offset.y = SCREENHEIGHT / 2 - self.player.rect.centery
        health_bar_rect = pygame.Rect(self.rect.centerx + offset.x -self.health_bar_length//2, self.rect.top + offset.y - 15, self.health_bar_length, self.health_bar_height)
        
        # Calculate health ratio and current width
        health_ratio = self.health / self.max_health
        bar_width = self.health_bar_length * health_ratio
        current_health_bar_rect = pygame.Rect(self.rect.centerx + offset.x - self.health_bar_length//2 , self.rect.top+ offset.y - 15, bar_width, self.health_bar_height)
        # Draw the health bar 
        if bar_width > 0:  # Only draw if there's health left
            pygame.draw.rect(screen, "black", health_bar_rect)
            pygame.draw.rect(screen, "white", current_health_bar_rect)



    def update(self):
        self.move()
        if not self.player.game_over:
            self.check_player_collision()

        if self.attacked:
            self.counter -= 1
            if self.counter < 0:
                self.counter = self.attack_cooldown
                self.attacked = False

class Orb(Entity):
    def __init__(self, groups, position, image: pygame.Surface, direction, parameters: dict):
        super().__init__(groups, position, image)
        self.speed = 10
        self.velocity = pygame.math.Vector2(direction) * self.speed
        self.collision_with_mob = False
        if parameters:
            self.mob_group = parameters["mob_group"]
            self.player = parameters["player"]
            self.wand = parameters["wand"]
        self.damage = self.wand.damage


    def move(self):
        self.rect.topleft += self.velocity
        self.check_collisions()
    def get_distance(self):
        return abs(math.sqrt((self.rect.x - self.player.rect.x)**2 + (self.rect.y - self.player.rect.y)**2))

    def check_collisions(self):
        # Reset the collision flag before checking
        self.collision_with_mob = False

        
        # Check collisions with entities in the groups
        for entity in self.mob_group:
            if isinstance(entity, Mob):
                if entity.rect.colliderect(self.rect):
                    # Set the collision flag
                    entity.health -= self.damage
                    self.collision_with_mob = True
                    #print(entity.health)
                    if entity.health <= 0:
                        entity.kill()
                    break 


    def handle_mob_collision(self):
        # Handle collision with Mob (e.g., apply damage, effects)
        if self.collision_with_mob == True or self.get_distance() > 20*TILESIZE:
            self.kill()  # Remove the orb from all groups
    def update(self):
        self.move()
        self.handle_mob_collision()