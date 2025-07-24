from player import Player
from utils import find_mutual_xcenter, normalize_state_agents, normalize_state_obstacles, normalize_state_interactables 
from levels import get_levels

import pygame
import random

class Game:
    def __init__(self, level_index):
        pygame.init()
        pygame.display.set_caption('Pico Park')
        self.screen_width, self.screen_height = 1200, 800
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        
        self.agents = [
            Player((100, 620)), # blue
            Player((200, 620), 'yellow'),
            Player((300, 620), 'red'),
            Player((400, 620), 'green')
        ]
        self.agents = []
        self.agent_actions = ['stand', 'jump', 'left', 'right']
        
        level = get_levels()[level_index]

        self.static_obstacles = level["static_obstacles"]
        self.door = level["door"]
        self.key = level["key"]
        self.button = level["button"]
            
            
    def interact_object(self, a):
        if self.key and a.rect.colliderect(self.key.rect) and not self.key.holder: # Get key
            self.key.collect(a)
            a.has_key = True
        
        if self.door and a.rect.colliderect(self.door.rect) and a.has_key: # Open door
            self.door.toggle()
            self.key.used = True
            
        if a.rect.colliderect(self.door.rect) and self.door.is_open:
            self.agents.remove(a)
            
        if self.button and a.rect.colliderect(self.button.rect) and not self.button.is_pressed:
            self.button.toggle()
       
                
    def move_objects(self, xmin_limit, xmax_limit, dt):        
        for ap in self.agents:
            obstacles = self.static_obstacles + [x.rect for x in self.agents if x != ap]
            ap.move_and_collide(obstacles, xmin_limit, xmax_limit, dt)
            ap.update_sprite(dt)
        
            # Check if fallen off screen end game
            if ap.y > self.screen_height:
                self.done = True

    
    def normalize_xposition(self, x, xmin, xmax):
        return (x - xmin) / (xmax - xmin) 
    
    def normalize_yposition(self, y):
        return y / self.screen_height 
    
    def get_state(self, xmin_limit, xmax_limit):
        state_obstacles = []
        state_agents = []
        state_interactables = []
        
        # Get static obstacles clipped to screen
        for obj in self.static_obstacles:
            if obj.right > xmin_limit and obj.height > 0:
                clipped_obj = [max(xmin_limit, obj.left), min(xmax_limit, obj.right), obj.top, obj.bottom]
                state_obstacles.append(clipped_obj)
                
        # Get agents data
        for a in self.agents:
            state_agents.append([a.id, a.x, a.y, a.vx, a.vy, a.is_jumping, a.has_key])
            
        state_interactables.append(self.door.positionxy + [self.door.is_open])
        state_interactables.append(self.button.positionxy)
        state_interactables.append(self.key.positionxy)
            
        return [
            normalize_state_obstacles(state_obstacles, xmin_limit, xmax_limit, self.screen_height),
            normalize_state_agents(state_agents, xmin_limit, xmax_limit, self.screen_height),
            normalize_state_interactables(state_interactables, xmin_limit, xmax_limit, self.screen_height)
        ]
                
    def step(self, agent_id, defined_action):
        dt = self.clock.tick(60) / 1000 # seconds since last frame
        agent = [a for a in self.agents if a.id == agent_id][0]

        mutual_xcenter = find_mutual_xcenter(self.agents) - (self.screen_width // 2)
        xmin_limit = mutual_xcenter 
        xmax_limit = mutual_xcenter + self.screen_width
        
        state = self.get_state()
        action = random.choice(self.agent_actions) if not defined_action else defined_action
        reward = self.get_policy_reward()
        
        agent.handle_input(action, dt)
        
        self.move_objects(xmin_limit, xmax_limit, dt)
        self.interact_object()
        
        if not self.agents:  # All agents have exited through the door
            self.done = True
            
        return state, action, reward, self.done
            