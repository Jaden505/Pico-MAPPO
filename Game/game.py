from player import Player
from utils import find_mutual_xcenter, event_to_action
from entities.door import Door
from entities.key import Key
from entities.button import Button
from levels import get_levels

import pygame
import sys

class Game:
    def __init__(self, level_index):
        pygame.init()
        pygame.display.set_caption('Pico Park')
        screen_width, screen_height = 1200, 800
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        self.player = Player((100, 620))  # on floor (700 - 80)
        self.agents = [
            Player((200, 620), 'yellow'),
            Player((300, 620), 'red'),
            Player((400, 620), 'green')
        ]
        self.agents = []

        self.agents_and_player = self.agents + [self.player]
        
        level = get_levels()[level_index]

        self.static_obstacles = level["static_obstacles"]
        self.door = level["door"]
        self.key = level["key"]
        self.button = level["button"]
        
    def draw_objects(self, offset, dt):
        self.screen.fill((240,240,240)) # Beige background
        
        for g in self.static_obstacles:
            # draw with scroll offset
            pygame.draw.rect(self.screen, (245, 141, 86), (g.x - offset[0], g.y - offset[1], g.width, g.height))
            
        self.door.draw(self.screen, offset)
       
        if self.key:
            self.key.draw(self.screen, offset, dt)
       
        if self.button:
            self.button.draw(self.screen, offset)
            
        for a in self.agents_and_player:
            self.screen.blit(a.sprite, (a.x - offset[0], a.y - offset[1]))
            
            
    def interact_object(self):
        for a in self.agents_and_player:
            
            if self.key and a.rect.colliderect(self.key.rect) and not self.key.holder: # Get key
                self.key.collect(a)
                a.has_key = True
            
            if self.door and a.rect.colliderect(self.door.rect) and a.has_key: # Open door
                self.door.toggle()
                self.key.used = True
                
            if a.rect.colliderect(self.door.rect) and self.door.is_open:
                self.agents_and_player.remove(a)
                
            if self.button and a.rect.colliderect(self.button.rect) and not self.button.is_pressed:
                self.button.toggle()
                
    def move_objects(self, xmin_limit, xmax_limit, dt):        
        for ap in self.agents_and_player:
            obstacles = self.static_obstacles + [x.rect for x in self.agents_and_player if x != ap]
            ap.move_and_collide(obstacles, xmin_limit, xmax_limit, dt)
            ap.update_sprite(dt)
        
            # Check if fallen off screen end game
            if ap.y > self.screen.get_height():
                self.exit()
                
    def run_game(self, headless_training=False):
        while True:
            dt = self.clock.tick(60) / 1000 # seconds since last frame

            mutual_xcenter = find_mutual_xcenter(self.agents_and_player) - (self.screen.get_width() // 2)
            xmin_limit = mutual_xcenter 
            xmax_limit = mutual_xcenter + self.screen.get_width()
            
            self.draw_objects([mutual_xcenter, 0], dt)
            self.move_objects(xmin_limit, xmax_limit, dt)
            self.interact_object()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                action = event_to_action(event, self.player.vx)
                self.player.handle_input(action, dt)
                    
            if not headless_training:
                pygame.display.update()
            
            if not self.agents_and_player:  # All agents have exited through the door
                self.exit()
                
    def exit(self):
        pygame.quit()
        sys.exit()
            
Game(5).run_game(headless_training=False)
