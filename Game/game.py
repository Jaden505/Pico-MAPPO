from player import Player
from utils import check_if_on_ground

import pygame
import pymunk
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pico Park')
        
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.player = Player((1100, 600))
        self.grounds = [pygame.Rect(0, 700, 1200, 100), pygame.Rect(400, 600, 400, 200)]
        
        self.sprite_width = self.player.sprite.get_width()
        self.sprite_height = self.player.sprite.get_height()
        
        
    def draw_objects(self):
        self.screen.fill((240,240,240)) # Beige background
        self.screen.blit(self.player.sprite, (self.player.x, self.player.y)) # Draw sprite 
        for g in self.grounds:
            pygame.draw.rect(self.screen, (245, 141, 86), g) # Draw ground
        
    def run_game(self):
        while True:
            dt = self.clock.tick(60) / 1000 # seconds since last frame
            self.space.step(1/60) # Update simulator space
            
            self.draw_objects()
            
            on_ground = check_if_on_ground(self.player, self.grounds, self.sprite_width, self.sprite_height)
            self.player.move_controls(on_ground, dt)
            self.player.update_sprite(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                self.player.set_controls(event, dt)
                    
            pygame.display.update()
            
Game().run_game()
