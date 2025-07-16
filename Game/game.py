from player import Player
from utils import find_mutual_xcenter

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
        
    def draw_objects(self, offset):
        self.screen.fill((240,240,240)) # Beige background
        self.screen.blit(self.player.sprite, (self.player.x - offset[0], self.player.y - offset[1])) # Draw sprite 
        
        for g in self.static_obstacles:
            # draw with scroll offset
            pygame.draw.rect(self.screen, (245, 141, 86), (g.x - offset[0], g.y - offset[1], g.width, g.height))
            
        for a in self.agents:
            self.screen.blit(a.sprite, (a.x - offset[0], a.y - offset[1]))
            
    def move_objects(self, dt):        
        agents_and_player = self.agents + [self.player]
        
        for ap in agents_and_player:
            obstacles = self.static_obstacles + [x.foot_hitbox for x in agents_and_player if x != ap]
            ap.move_and_collide(obstacles, dt)
            ap.update_sprite(dt)
        
    def run_game(self):
        while True:
            dt = self.clock.tick(60) / 1000 # seconds since last frame

            mutual_xcenter = find_mutual_xcenter(self.player, self.agents) - (self.screen.get_width() // 2)
            
            self.draw_objects([mutual_xcenter, 0])
            self.move_objects(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                self.player.on_key_update(event, dt)
                    
            pygame.display.update()
            
Game(headless_training=False).run_game()
