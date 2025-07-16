from player import Player

import pygame
import sys

class Game:
    def __init__(self, headless_training=False):
        pygame.init()
        pygame.display.set_caption('Pico Park')
        
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.player = Player((1100, 600))
        self.agents = [Player((900, 600), 'yellow'), Player((100, 600), 'red'), Player((500, 300), 'green')]
        self.static_obstacles = [pygame.Rect(0, 700, 1200, 100), pygame.Rect(400, 600, 400, 200)]
        
        self.sprite_width = self.player.sprite.get_width()
        self.sprite_height = self.player.sprite.get_height()
        
    def draw_objects(self):
        self.screen.fill((240,240,240)) # Beige background
        self.screen.blit(self.player.sprite, (self.player.x, self.player.y)) # Draw sprite 
        
        for g in self.static_obstacles:
            pygame.draw.rect(self.screen, (245, 141, 86), g) # Draw ground
            
        for a in self.agents:
            self.screen.blit(a.sprite, (a.x, a.y)) # Draw sprite 
            
    def move_objects(self, dt):        
        agents_and_player = self.agents + [self.player]
        
        for ap in agents_and_player:
            obstacles = self.static_obstacles + [x.foot_hitbox for x in agents_and_player if x != ap]
            ap.move_and_collide(obstacles, dt)
            ap.update_sprite(dt)
        
    def run_game(self):
        while True:
            dt = self.clock.tick(60) / 1000 # seconds since last frame
            
            self.draw_objects()
            self.move_objects(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                self.player.on_key_update(event, dt)
                    
            pygame.display.update()
            
Game(headless_training=False).run_game()
