from player import Player

import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pico Park')
        pygame.event.pump() 
        dt = 0.1
        
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.player = Player((1100, 700), dt)
        
    def run(self):
        while True:
            self.screen.fill((240,240,240)) # Beige background
            
            self.player.move_controls()
            self.player.update_sprite()
            self.screen.blit(self.player.sprite, (self.player.x, self.player.y)) # Draw sprite 
             
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                self.player.set_controls(event)
                    
            pygame.display.update()
            self.clock.tick(60)
            
Game().run()
