from player import Player
from utils import find_mutual_xcenter, event_to_action
from entities.door import Door
from entities.key import Key
from entities.button import Button

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
        self.agents_and_player = self.agents + [self.player]
        
        self.static_obstacles = [
            pygame.Rect(0, 700, 5000, 100), # Floor
            pygame.Rect(1400, 600, 1000, 500), # Platform right
            pygame.Rect(500, 0, 100, 800), # Middle wall
            pygame.Rect(1200, 600, 200, 0), # Bridge
            pygame.Rect(0, 0, 100, 800), # Left wall
        ]
        
        self.door = Door((2100, 600))
        self.key = Key((1200, 600))
        # self.button = Button((1500, 600), self.static_obstacles[2], 'dissapear')
        self.button = Button((1500, 600), self.static_obstacles[3], 'appear', appear_height=200)
        
    def draw_objects(self, offset, dt):
        self.screen.fill((240,240,240)) # Beige background
        
        for g in self.static_obstacles:
            # draw with scroll offset
            pygame.draw.rect(self.screen, (245, 141, 86), (g.x - offset[0], g.y - offset[1], g.width, g.height))
            
        self.door.draw(self.screen, offset)
        self.key.draw(self.screen, offset, dt)
        self.button.draw(self.screen, offset)
            
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
                
            if a.rect.colliderect(self.button.rect) and not self.button.is_pressed:
                self.button.toggle()
                
    def move_objects(self, dt):        
        for ap in self.agents_and_player:
            obstacles = self.static_obstacles + [x.rect for x in self.agents_and_player if x != ap]
            ap.move_and_collide(obstacles, dt)
            ap.update_sprite(dt)
        
        
    def run_game(self):
        while True:
            dt = self.clock.tick(60) / 1000 # seconds since last frame

            mutual_xcenter = find_mutual_xcenter(self.agents_and_player) - (self.screen.get_width() // 2)
            xmin_limit = mutual_xcenter - self.screen.get_width() // 2
            xmax_limit = mutual_xcenter + self.screen.get_width() // 2
            print(xmin_limit, xmax_limit)
            
            self.draw_objects([mutual_xcenter, 0], dt)
            self.move_objects(dt, xmin_limit, xmax_limit)
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
