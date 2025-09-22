from Game.player import Player
from Game.utils import find_outer_x_limits, event_to_action
from Game.levels import get_levels

import pygame
import sys, time

class Game:
    def __init__(self, level_index):
        pygame.init()
        pygame.display.set_caption('Pico Park')
        self.screen_width, self.screen_height = 1200, 800
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        
        self.player = Player((100, 620))  # on floor (700 - 80)
        self.agents = [
            # Player((200, 620), 'yellow'),
            # Player((300, 620), 'red'),
            # Player((400, 620), 'green')
        ]

        self.agents_and_player = self.agents + [self.player]
        
        level = get_levels()[level_index]

        self.static_obstacles = level["static_obstacles"]
        self.door = level["door"]
        self.key = level["key"]
        self.button = level["button"]
        self.coins = level["coins"]
        
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
            
        for c in self.coins:
            pygame.draw.ellipse(self.screen, (255, 223, 0), (c.x - offset[0], c.y - offset[1], c.width, c.height))
            
            
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
            if ap.y > self.screen_height:
                self.exit()
                
    def run_game(self):
        while True:
            dt = self.clock.tick(60) / 1000 # seconds since last frame

            xmin_limit, xmax_limit = find_outer_x_limits(self.agents_and_player, self.screen_width)
            
            self.draw_objects((xmin_limit, 0), dt)
            self.move_objects(xmin_limit, xmax_limit, dt)
            self.interact_object()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                action = event_to_action(event, self.player.vx)

                self.player.handle_input(action, dt)
                
            if not self.agents_and_player:  # All agents have exited through the door
                self.exit()
                
            pygame.display.flip()
                
    def exit(self):
        pygame.quit()
        sys.exit()
            
