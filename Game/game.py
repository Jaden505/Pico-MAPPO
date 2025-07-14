from player import Player
from utils import check_if_on_ground

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
        self.player = Player((1100, 600), dt)
        self.grounds = [pygame.Rect(0, 700, 1200, 100), pygame.Rect(400, 600, 400, 200)]
        
        self.sprite_width = self.player.sprite.get_width()
        self.sprite_height = self.player.sprite.get_height()

        
    def run(self):
        while True:
            self.screen.fill((240,240,240)) # Beige background

            self.screen.blit(self.player.sprite, (self.player.x, self.player.y)) # Draw sprite 
            
            for g in self.grounds:
                pygame.draw.rect(self.screen, (245, 141, 86), g) # Draw ground
            
            on_ground = check_if_on_ground(self.player, self.grounds, self.sprite_width, self.sprite_height)
            self.player.move_controls(on_ground)
            self.player.update_sprite()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                self.player.set_controls(event)
                    
            pygame.display.update()
            self.clock.tick(60)
            
Game().run()
