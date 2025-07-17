from player import Player
from utils import find_mutual_xcenter, event_to_action

import pygame
import sys

class Game:
    def __init__(self, headless_training=False):
        pygame.init()
        pygame.display.set_caption('Pico Park')
        screen_width, screen_height = 1200, 800
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.player = Player((1100, 400))
        self.agents = [Player((900, 400), 'yellow'), Player((1000, 400), 'red'), Player((800, 400), 'green')]
        self.static_obstacles = [
            pygame.Rect(0, 700, 12000, 100), # Floor
            ]
        self.objectives = [
            
        ]
        
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
                    
                action = event_to_action(event, self.player.vx)
                self.player.handle_input(action, dt)
                    
            pygame.display.update()
            
Game(headless_training=False).run_game()
