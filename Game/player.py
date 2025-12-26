from game.utils import PLAYER_COLOR_MAPS, SPRITES_DIR, load_sprite
from game.no_pygame_rect import Rect

import pygame
import cv2
import os

class Player:
    def __init__(self, init_pos, color='blue', visualize=False):
        color_map = PLAYER_COLOR_MAPS[color] if color != 'blue' else {}
        
        if visualize:
            # Sprites    
            self.stand_right = load_sprite('pico_stand.png', color_map=color_map)
            self.stand_left = pygame.transform.flip(self.stand_right, True, False)
            
            self.walk_right = [load_sprite(f'pico_move{i}.png', color_map=color_map) for i in range(1, 5)]
            self.walk_left = [pygame.transform.flip(img, True, False) for img in self.walk_right]
            
            self.push_right = [load_sprite(f'pico_push{i}.png', color_map=color_map) for i in range(1, 5)]
            self.push_left = [pygame.transform.flip(img, True, False) for img in self.push_right]
            
            self.jump_right = load_sprite('pico_jump.png', color_map=color_map)
            self.jump_left = pygame.transform.flip(self.jump_right, True, False)
            
            self.sprite = self.stand_right
            
            self.width = self.sprite.get_width()
            self.height = self.sprite.get_height()
            
            # Extras
            self.cycle_ind = 0 # Which run sprite image to show in sequence
            self.cycle_len = len(self.walk_right)
            self.anim_timer = 0
            self.anim_speed = 0.15  # seconds per frame
        else:
            sprite_path = os.path.join(SPRITES_DIR, 'pico_stand.png')
            default_sprite = cv2.imread(sprite_path, cv2.IMREAD_UNCHANGED)
            self.width, self.height = default_sprite.shape[1], default_sprite.shape[0]
        
        # Orientation
        self.facing_left = False
        self.jumping = True # start in air to avoid initial collision issues
        self.pushing = False
        
        self.init_pos = init_pos
        self.x, self.y = init_pos[0], init_pos[1]
        self.vx, self.vy = 0, 0
        self.acx, self.acy = 10000, 45000 
        
        self.jump_gravity = 40
        
        self.rect = Rect(self.x, self.y, self.width, self.height)
        
        # Extras
        self.has_key = False
        self.id = color_map.get('id', 1) 
        
        
    def update_sprite(self, dt):
        if self.vx == 0 and self.vy == 0 and not self.jumping: # standing still
            self.sprite = self.stand_left if self.facing_left else self.stand_right
            
        elif self.jumping:
            self.sprite = self.jump_left if self.facing_left else self.jump_right
            
        elif self.pushing:
            self.cycle_sprites(self.push_left if self.facing_left else self.push_right, dt)
            
        else: # walking
            self.cycle_sprites(self.walk_left if self.facing_left else self.walk_right, dt)


    def handle_input(self, key, dt):
        if key == 'left':
            self.vx = -self.acx * dt
            self.facing_left = True
        if key == 'right':
            self.vx = self.acx * dt
            self.facing_left = False
        if key == 'jump' and not self.jumping:
            self.jumping = True
            self.vy = -self.acy * dt           
        if key == 'stand':
            self.vx = 0
        

    def move_and_collide(self, static_obstacles, xmin_limit, xmax_limit, dt):     
        self.x += self.vx * dt
        self.rect.x = self.x
        
        self.pushing = False
        
        # Horizontal collision
        for obs in static_obstacles:
            if self.foot_hitbox.colliderect(obs): 
                if self.vx > 0 and obs.left > self.x: # hit right wall
                    self.x = obs.left - self.width * 3/4
                    self.pushing = True

                elif self.vx < 0 and obs.left < self.x: # hit left wall
                    self.x = obs.right - self.width * 1/4
                    self.pushing = True
                    
                self.rect.x = self.x
                if self.foot_hitbox.colliderect(obs):
                    self.vx = 0
                    
        # Limit horizontal movement
        self.x = max(xmin_limit, min(self.x, xmax_limit))
                         
        if self.vy < self.acy: # apply jump gravity
            self.vy += self.jump_gravity
            
        self.y += self.vy * dt       
        self.rect.y = self.y
        
        # Vertical collision
        for obs in static_obstacles:
            if self.foot_hitbox.colliderect(obs):   
                if self.vy > 0: # hit floor
                    self.y = obs.top - self.height
                    self.jumping = False
                    
                elif self.vy < 0: # hit ceiling
                    self.y = obs.bottom
                    self.jumping = False
                    
                self.vy = 0
                self.rect.y = self.y

    def cycle_sprites(self, sprites, dt):
        """Helper function to cycle through a list of sprites."""
        self.anim_timer += dt
        
        if self.anim_timer > self.anim_speed:
            self.sprite = sprites[self.cycle_ind]
            self.cycle_ind = (self.cycle_ind + 1) % len(sprites)
            self.anim_timer = 0
          
    @property
    def foot_hitbox(self):
        return Rect(
            self.rect.x + self.width/4,
            self.rect.top,
            self.rect.width/2.,
            self.height
        )
                
    def __eq__(self, value): # Differentiate between Players based on their initial position
        return self.id == value
