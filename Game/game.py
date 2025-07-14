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
        self.player = Player((1100, 600), dt)
        self.ground = pygame.Rect(0, 700, 1200, 100)
        
        self.sprite_width, self.sprite_height = self.player.sprite.get_width(), self.player.sprite.get_height()+1
        
    def run(self):
        while True:
            self.screen.fill((240,240,240)) # Beige background
            
            player_r = pygame.Rect(self.player.x, self.player.y, 
                                   self.sprite_width, self.sprite_height)
            
            self.screen.blit(self.player.sprite, (self.player.x, self.player.y)) # Draw sprite 
            pygame.draw.rect(self.screen, (245, 141, 86), self.ground) # Draw ground
            
            self.player.move_controls(player_r.colliderect(self.ground))
            self.player.update_sprite()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                self.player.set_controls(event)
                    
            pygame.display.update()
            self.clock.tick(60)
            
Game().run()
