import pygame
import sys
from globals import *
from scene import Scene
from events import EventHandler
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        icon = pygame.image.load('res/heart.png')  

        # Set the window icon
        pygame.display.set_icon(icon)   
        pygame.display.set_caption("terrarossa - bitaneme") 
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.load("res/background_music.mp3")
        pygame.mixer.music.play(-1)      



        self.scene = Scene(self)
    
    def run(self):
        while self.scene.running:
            self.update()
            self.draw()

        self.close()
    def update(self):
        EventHandler.poll_events()
        for event in EventHandler.events:
            if event.type == pygame.QUIT:
                self.scene.running = False

        self.scene.update()
    
        pygame.display.update()
        self.clock.tick(FPS)

    def draw(self):
        self.scene.draw()
    
    def close(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()