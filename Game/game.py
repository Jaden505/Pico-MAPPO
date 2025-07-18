from player import Player
from utils import find_mutual_xcenter, event_to_action
from entities.door import Door
from entities.key import Key

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
        self.agents = []
        self.agents_and_player = self.agents + [self.player]
        
        self.static_obstacles = [
            pygame.Rect(0, 700, 5000, 100), # Floor
            pygame.Rect(1400, 600, 500, 500), # Platform
            pygame.Rect(1900, 600, 500, 2000), 
            ]
        
        self.door = Door((2100, 600))
        self.key = Key((1200, 400))
        
    def draw_objects(self, offset, dt):
        self.screen.fill((240,240,240)) # Beige background
        
        for g in self.static_obstacles:
            # draw with scroll offset
            pygame.draw.rect(self.screen, (245, 141, 86), (g.x - offset[0], g.y - offset[1], g.width, g.height))
            
        self.door.draw(self.screen, offset)
        self.key.draw(self.screen, offset, dt)
            
        for a in self.agents_and_player:
            self.screen.blit(a.sprite, (a.x - offset[0], a.y - offset[1]))
            
            
    def interact_object(self):
        for a in self.agents_and_player:
            
            if a.rect.colliderect(self.key.rect) and not self.key.holder: # Get key
                self.key.collect(a)
                a.has_key = True
            
            if a.rect.colliderect(self.door.rect) and a.has_key: # Open door
                self.door.toggle()
                self.key.used = True
                
            if a.rect.colliderect(self.door.rect) and self.door.is_open:
                self.agents_and_player.remove(a)
                
                
    def move_objects(self, dt):        
        for ap in self.agents_and_player:
            obstacles = self.static_obstacles + [x.foot_hitbox for x in self.agents_and_player if x != ap]
            ap.move_and_collide(obstacles, dt)
            ap.update_sprite(dt)
        
        
    def run_game(self):
        while True:
            dt = self.clock.tick(60) / 1000 # seconds since last frame

            mutual_xcenter = find_mutual_xcenter(self.agents_and_player) - (self.screen.get_width() // 2)
            
            self.draw_objects([mutual_xcenter, 0], dt)
            self.move_objects(dt)
            self.interact_object()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                action = event_to_action(event, self.player.vx)
                self.player.handle_input(action, dt)
                    
            pygame.display.update()
            
            if not self.agents_and_player:  # All agents have exited through the door
                pygame.quit()
                sys.exit()
            
Game(headless_training=False).run_game()
