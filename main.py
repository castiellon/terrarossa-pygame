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
        self.font_big = pygame.font.Font("res/font.ttf", 74)
        self.font_small = pygame.font.Font("res/font.ttf", 40)
        self.background_image = pygame.image.load("res/credits.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (SCREENWIDTH,SCREENHEIGHT))
        self.background_image_2 = pygame.image.load("res/credits_2.png").convert_alpha()
        self.background_image_2 = pygame.transform.scale(self.background_image_2, (SCREENWIDTH,SCREENHEIGHT))
        # Set the window icon
        pygame.display.set_icon(icon)   
        pygame.display.set_caption("terrarossa - bitaneme") 
        




        self.scene = Scene(self)

    def main_menu(self): 
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load("res/start_menu.mp3")
        pygame.mixer.music.play(-1)     

        title_text = self.font_big.render("terrarossa", True, "white")
        start_text = self.font_small.render("Press ENTER to Start", True, "white")
        exit_text = self.font_small.render("Press ESC to Exit", True, "white")

        while True:
            self.screen.blit(self.background_image, (0, 0))  # Draw the background image
            self.screen.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 100))
            self.screen.blit(start_text, (SCREENWIDTH // 2 - start_text.get_width() // 2, 400))
            self.screen.blit(exit_text, (SCREENWIDTH // 2 - exit_text.get_width() // 2, 500))
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

    
    def credits(self):
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load("res/across_the_desert.mp3")
        pygame.mixer.music.play(1)    

        title_text = self.font_big.render("credits", True, "white")
        credit_text = self.font_big.render("game by talha", True, "white")
        exit_text = self.font_big.render("press ESC to exit", True, "white")

        while True:
            self.screen.blit(self.background_image, (0, 0))  # Draw the background image
            self.screen.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 100))
            self.screen.blit(credit_text, (SCREENWIDTH // 2 - credit_text.get_width() // 2, 250))
            self.screen.blit(exit_text, (SCREENWIDTH // 2 - exit_text.get_width() // 2, 350))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()  # Close the game properly
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()  # Close the game properly
                        return
    def pause(self):
        pygame.mixer.music.pause()
        title_text = self.font_big.render("paused", True, "white")
        exit_text = self.font_small.render("press ESC to return", True, "white")

        while True:
            self.screen.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 20))
            self.screen.blit(exit_text, (SCREENWIDTH // 2 - exit_text.get_width() // 2, 200))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()  # Close the game properly
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.scene.running = True  # Start the game
                        pygame.mixer.music.unpause()
                        return
    def finale(self):
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load("res/jazz_on_a_boat.mp3")
        pygame.mixer.music.play(1)  
        
        title_text = self.font_big.render("you won!!", True, "black")
        credit_text = self.font_big.render("game by talha", True, "black")
        exit_text = self.font_big.render("press ESC to exit", True, "black")
        while True:
            self.screen.blit(self.background_image_2, (0, 0))  # Draw the background image
            self.screen.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 100))
            self.screen.blit(credit_text, (SCREENWIDTH // 2 - credit_text.get_width() // 2, 250))
            self.screen.blit(exit_text, (SCREENWIDTH // 2 - exit_text.get_width() // 2, 350))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()  # Close the game properly
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()  # Close the game properly
                        return

    def run(self):
        self.main_menu()  # Show the main menu first
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load("res/background_music.mp3")
        pygame.mixer.music.play(-1)    
        while True:  # Use an infinite loop to manage states
            if self.scene.running:
                self.update()
                self.draw()
            elif not self.scene.running:
                if self.scene.player.game_over:
                    self.credits()  # Credits
                else:
                    self.finale() #won the game


            
    def update(self):
        EventHandler.poll_events()
        for event in EventHandler.events:
            if event.type == pygame.QUIT :
                self.close()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    self.pause()
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