from game.player import Player
from game.utils import *
from game.levels import get_levels

import pygame
import numpy as np

class GameEnvironment:
    def __init__(self, level_index, visualize):
        self.level_index = level_index
        self.visualize = visualize
        
        self.screen_width, self.screen_height = 1200, 800
        if visualize:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            self.clock = pygame.time.Clock()
        
        self.agents = [
            Player((100, 600)), # blue
            Player((250, 600), 'yellow'),
            Player((400, 600), 'red'),
            Player((550, 600), 'green')
        ]
        
        self.agent_actions = ['stand', 'jump', 'left', 'right']
        self.state_space_shape = (10*4) + (4*7) + (3*3)  # obstacles, agents, interactables
        self.action_space_shape = len(self.agent_actions) 
        
        level = get_levels()[level_index] 

        self.static_obstacles = level["static_obstacles"]
        self.door = level["door"]
        self.key = level["key"]
        self.button = level["button"]
        self.coins = level["coins"]
        self.level = level
        
        self.done = False
        self.reward = 0
            
    def interact_object(self, a):
        if self.key and a.rect.colliderect(self.key.rect) and not self.key.holder: # Get key
            self.key.collect(a)
            a.has_key = True
            self.reward += 3
        
        if self.door and a.rect.colliderect(self.door.rect) and a.has_key: # Open door
            self.door.toggle()
            self.key.used = True
            self.reward += 4
            
        if a.rect.colliderect(self.door.rect) and self.door.is_open: # Exit through door
            self.agents.remove(a)
            self.reward += 4
            
        if self.button and a.rect.colliderect(self.button.rect) and not self.button.is_pressed: # Press button
            self.button.toggle()
            self.reward += 3
       
                
    def move_objects(self, xmin_limit, xmax_limit, dt):        
        for ap in self.agents:
            obstacles = self.static_obstacles + [x.rect for x in self.agents if x != ap]
            ap.move_and_collide(obstacles, xmin_limit, xmax_limit, dt)
            ap.update_sprite(dt)
        
            # Check if off screen end game
            if ap.y > self.screen_height or ap.y < 0:
                self.done = True
                self.reward -= 5  # Penalty for dying
                
    
    def get_state(self):
        state_obstacles = []
        state_agents = []
        state_interactables = []
        
        xmin_limit, xmax_limit = find_outer_x_limits(self.agents, self.screen_height)
        
        # Get static obstacles clipped to screen
        for obj in self.static_obstacles:
            if obj.right > xmin_limit and obj.height > 0:
                clipped_obj = [max(xmin_limit, obj.left), min(xmax_limit, obj.right), obj.top, obj.bottom]
                state_obstacles.append(clipped_obj)
                
        for i in range(len(state_obstacles), 10):  # Pad with empty obstacles if less than 10
            state_obstacles.append([0, 0, 0, 0])
                
        # Get agents data
        for a in self.agents:
            state_agents.append([a.id, a.x, a.y, a.vx, a.vy, a.jumping, a.has_key])
            
        for i in range(len(state_agents), 4):  # Pad with empty agents if less than 4
            state_agents.append([0, 0, 0, 0, 0, 0, 0])
                    
        # Get interactables data
        state_interactables.append(self.door.positionxy + [self.door.is_open])
        state_interactables.append(self.button.positionxy + [self.button.is_pressed] if self.button else [0, 0, 0])
        state_interactables.append(self.key.positionxy + [self.key.used] if self.key else [0, 0, 0])
        
        for i in state_interactables: # Set positions outside limits to 0
            if i[0] < xmin_limit or i[0] > xmax_limit:
                i[0] = i[1] = 0
        
        return np.concatenate((
            normalize_state_obstacles(state_obstacles, xmin_limit, xmax_limit, self.screen_height), # shape 10
            normalize_state_agents(state_agents, xmin_limit, xmax_limit, self.screen_height), # shape 4
            normalize_state_interactables(state_interactables, xmin_limit, xmax_limit, self.screen_height) # shape 3
        ))
                
    def step(self, agent_id, action_ind):
        self.reward = 0
        agent = [a for a in self.agents if a.id == agent_id][0]
        
        if self.visualize:
            dt = self.clock.tick(60) / 1000 # seconds since last frame
        else:
            dt = 0.016  # Assume ~60 FPS for non-visualized runs

        xmin_limit, xmax_limit = find_outer_x_limits(self.agents, self.screen_height)
        
        action = self.agent_actions[action_ind]
        # agent.handle_input(action, dt)
        
        if self.visualize:
            self.draw_objects((xmin_limit, 0), dt)
        
        prev_dist = abs(self.door.left - agent.x) # Distance to door before move
        # self.move_objects(xmin_limit, xmax_limit, dt)
        curr_dist = abs(self.door.left - agent.x)
        
        self.interact_object(agent)
        
        self.reward -= 0.05  # Small penalty for each step taken
        self.reward += (prev_dist - curr_dist) * 0.01 # Small reward for moving towards door
        
        if not self.agents:  # All agents have exited through the door
            self.done = True
            
            if all([a.y < self.screen_height for a in self.agents]):
                self.reward += 10 # Bonus for all agents exiting
                self.level['completed'] = True
            
        return self.get_state(), self.reward, self.done
            
            
    def reset(self, level_index):
        self.done = False
        self.reward = 0
        level = get_levels()[level_index]
        
        self.static_obstacles = level["static_obstacles"]
        self.door = level["door"]
        self.key = level["key"]
        self.button = level["button"]
        self.coins = level["coins"]
        self.level = level
        
        self.agents = [
            Player((100, 600)), # blue
            Player((250, 600), 'yellow'),
            Player((400, 600), 'red'),
            Player((550, 600), 'green')
        ]
        
        if self.visualize:
            for event in pygame.event.get(): # Must have this to process pygame events
                if event.type == pygame.QUIT:
                    break
       
    def draw_objects(self, offset, dt, show_coins=True):
        self.screen.fill((240,240,240)) # Beige background
        
        for g in self.static_obstacles:
            # draw with scroll offset
            pygame.draw.rect(self.screen, (245, 141, 86), (g.x - offset[0], g.y - offset[1], g.width, g.height))
            
        self.door.draw(self.screen, offset)
       
        if self.key:
            self.key.draw(self.screen, offset, dt)
       
        if self.button:
            self.button.draw(self.screen, offset)
            
        for a in self.agents:
            self.screen.blit(a.sprite, (a.x - offset[0], a.y - offset[1]))
            
        if show_coins:
            for c in self.coins:
                pygame.draw.ellipse(self.screen, (255, 223, 0), (c.x - offset[0], c.y - offset[1], c.width, c.height))
            

        pygame.display.flip()
        
            