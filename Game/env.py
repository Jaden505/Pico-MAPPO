from Game.player import Player
from Game.utils import *
from Game.levels import get_levels

import pygame

class Environment:
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
        
        self.agent_actions = ['stand', 'jump', 'left', 'right']
        self.state_space_shape = (10, 4, 3)  # obstacles, agents, interactables
        self.action_space_shape = len(self.agent_actions)
        
        level = get_levels()[level_index]

        self.static_obstacles = level["static_obstacles"]
        self.door = level["door"]
        self.key = level["key"]
        self.button = level["button"]
        
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
        
            # Check if fallen off screen end game
            if ap.y > self.screen_height:
                self.done = True
                self.reward -= 5  # Penalty for dying
                
    
    def get_state(self, xmin_limit, xmax_limit):
        state_obstacles = []
        state_agents = []
        state_interactables = []
        
        # Get static obstacles clipped to screen
        for obj in self.static_obstacles:
            if obj.right > xmin_limit and obj.height > 0:
                clipped_obj = [max(xmin_limit, obj.left), min(xmax_limit, obj.right), obj.top, obj.bottom]
                state_obstacles.append(clipped_obj)
                
        for i in range(len(state_obstacles), 10):  # Pad with empty obstacles if less than 10
            state_obstacles.append([0, 0, 0, 0])
                
        # Get agents data
        for a in self.agents:
            state_agents.append([a.id, a.x, a.y, a.vx, a.vy, a.is_jumping, a.has_key])
            
        for i in range(len(state_agents), 4):  # Pad with empty agents if less than 4
            state_agents.append([i, 0, 0, 0, 0, 0, 0])
        
        # Get interactables data
        state_interactables.append(self.door.positionxy + [self.door.is_open])
        state_interactables.append((self.button.positionxy + [self.button.is_pressed]) if self.button else [0, 0, 0])
        state_interactables.append([self.key.positionxy] if self.key else [0, 0, 0])
        
        return [
            normalize_state_obstacles(state_obstacles, xmin_limit, xmax_limit, self.screen_height), # shape 10
            normalize_state_agents(state_agents, xmin_limit, xmax_limit, self.screen_height), # shape 4
            normalize_state_interactables(state_interactables, xmin_limit, xmax_limit, self.screen_height) # shape 3
        ]
                
    def step(self, agent_id, action_probs):
        dt = self.clock.tick(60) / 1000 # seconds since last frame
        agent = [a for a in self.agents if a.id == agent_id][0]

        mutual_xcenter = find_mutual_xcenter(self.agents) - (self.screen_width // 2)
        xmin_limit = mutual_xcenter 
        xmax_limit = mutual_xcenter + self.screen_width
        
        reward = self.get_policy_reward(agent)
        
        action = self.agent_actions[action_probs.argmax()]
        agent.handle_input(action, dt)
        
        self.move_objects(xmin_limit, xmax_limit, dt)
        self.interact_object()
        
        self.reward -= 0.1  # Small penalty for each step taken
        self.reward += max(1, agent.x / self.door.position[0])  # Reward based on distance to door
        
        if not self.agents:  # All agents have exited through the door
            self.done = True
            
            if all([a.y < self.screen_height for a in self.agents]):
                self.reward += 10 # Bonus for all agents exiting
            
        return action, reward, self.done
            
            
    def reset(self, level_index):
        self.done = False
        self.reward = 0
        level = get_levels()[level_index]
        
        self.static_obstacles = level["static_obstacles"]
        self.door = level["door"]
        self.key = level["key"]
        self.button = level["button"]
        
        # Reset agents
        self.agents = [
            Player((100, 620)), # blue
            Player((200, 620), 'yellow'),
            Player((300, 620), 'red'),
            Player((400, 620), 'green')
        ]
       