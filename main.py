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
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load("res/background_music.mp3")
        pygame.mixer.music.play(-1)      



        self.scene = Scene(self)

    def main_menu(self):
        font = pygame.font.Font(None, 74)
        title_text = font.render("Main Menu", True, "white")
        start_text = font.render("Press ENTER to Start", True, "white")
        exit_text = font.render("Press ESC to Exit", True, "white")

        while True:
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.screen.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 100))
            self.screen.blit(start_text, (SCREENWIDTH // 2 - start_text.get_width() // 2, 250))
            self.screen.blit(exit_text, (SCREENWIDTH // 2 - exit_text.get_width() // 2, 350))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()  # Close the game properly
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.scene.running = True  # Start the game
                        return
                    elif event.key == pygame.K_ESCAPE:
                        self.close()  # Close the game properly
                        return

    
    def run(self):
        self.main_menu()  # Show the main menu first
        while True:  # Use an infinite loop to manage states
            if self.scene.running:
                self.update()
                self.draw()
            else:
                self.main_menu()  # Return to the menu if not running


            
    def update(self):
        EventHandler.poll_events()
        for event in EventHandler.events:
            if event.type == pygame.QUIT :
                self.close()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    self.scene.running = False 
                    return

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