from utils import recolor_image, PLAYER_COLOR_MAPS

import pygame

class Player:
    def __init__(self, init_pos, color='blue'):
        # Sprites
        color_map = PLAYER_COLOR_MAPS[color] if color != 'blue' else {}
        
        def load_and_recolor(path):
            img = pygame.image.load(path).convert_alpha()
            return recolor_image(img, color_map)
        
        self.stand_right = load_and_recolor('sprites/pico_stand.png')
        self.stand_left = pygame.transform.flip(self.stand_right, True, False)
        
        self.walk_right = [load_and_recolor(f'sprites/pico_move{i}.png') for i in range(1, 5)]
        self.walk_left = [pygame.transform.flip(img, True, False) for img in self.walk_right]
        
        self.push_right = [load_and_recolor(f'sprites/pico_push{i}.png') for i in range(1, 5)]
        self.push_left = [pygame.transform.flip(img, True, False) for img in self.push_right]
        
        self.jump_right = load_and_recolor('sprites/pico_jump.png')
        self.jump_left = pygame.transform.flip(self.jump_right, True, False)
        
        self.sprite = self.stand_right
        
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        
        # Orientation
        self.facing_left = False
        self.jumping = False
        self.pushing = False
        
        self.init_pos = init_pos
        self.x, self.y = init_pos[0], init_pos[1]
        self.vx, self.vy = 0, 0
        self.acx, self.acy = 10000, 800
        
        self.jump_gravity = 40
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Extras
        self.walk_cycle_ind = 0 # Which run sprite image to show in sequence
        self.push_cycle_ind = 0
        
        self.cycle_len = len(self.walk_right)
        self.anim_timer = 0
        self.anim_speed = 0.15  # seconds per frame
        
        
    def update_sprite(self, dt):
        if self.vx == 0 and self.vy == 0 and not self.jumping:
            self.sprite = self.stand_left if self.facing_left else self.stand_right
        elif self.jumping:
            self.sprite = self.jump_left if self.facing_left else self.jump_right
        elif self.pushing:
            self.anim_timer += dt
            
            if self.anim_timer > self.anim_speed:
                self.sprite = self.push_left[self.push_cycle_ind] if self.facing_left else self.push_right[self.push_cycle_ind]
                self.push_cycle_ind = self.push_cycle_ind+1 if self.push_cycle_ind < self.cycle_len-1 else 0
                self.anim_timer = 0
        else:
            self.anim_timer += dt
            
            if self.anim_timer > self.anim_speed:
                self.sprite = self.walk_left[self.walk_cycle_ind] if self.facing_left else self.walk_right[self.walk_cycle_ind]
                self.walk_cycle_ind = self.walk_cycle_ind+1 if self.walk_cycle_ind < self.cycle_len-1 else 0
                self.anim_timer = 0
        
    def on_key_update(self, event, dt):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.vx = -self.acx * dt
                self.facing_left = True
                
            if event.key == pygame.K_RIGHT:
                self.vx = self.acx * dt
                self.facing_left = False

            if event.key == pygame.K_SPACE and not self.jumping:
                self.jumping = True
                self.vy = -self.acy

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.vx < 0:
                self.vx = 0
            if event.key == pygame.K_RIGHT and self.vx > 0:
                self.vx = 0
                
                
    def on_agent_input(self, key, dt):
        if key == 'left':
            self.vx = -self.acx * dt
            self.facing_left = True
        if key == 'right':
            self.vx = self.acx * dt
            self.facing_left = False
        if key == 'jump' and not self.jumping:
            self.jumping = True
            self.vy = -self.acy            
        if key == 'stand':
            self.vx = 0
        

    def move_and_collide(self, static_obstacles, dt):     
        self.x += self.vx * dt
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.pushing = False
        
        # Horizontal collision
        for obs in static_obstacles:
            if self.rect.colliderect(obs): 
                if self.vx > 0: # hit right wall
                    self.x = obs.left - self.width
                    self.pushing = True

                elif self.vx < 0: # hit left wall
                    self.x = obs.right
                    self.pushing = True
                    
                self.rect.x = self.x
                if self.rect.colliderect(obs):
                    self.vx = 0
                         
        if self.vy < self.acy: # apply jump gravity
            self.vy += self.jump_gravity
            
            
        self.y += self.vy * dt       
        self.rect.y = self.y
        
        # Vertical collision
        for obs in static_obstacles:
            if self.rect.colliderect(obs):   
                if self.vy > 0: # hit floor
                    self.y = obs.top - self.height 
                    self.jumping = False
                    
                elif self.vy < 0: # hit ceiling
                    self.y = obs.bottom
                    self.jumping = False
                    
                self.vy = 0
                
    @property
    def foot_hitbox(self):
        return pygame.Rect(
            self.rect.x + self.width/4,
            self.rect.top,
            self.rect.width/2.,
            self.height
        )
                
    def __eq__(self, value):
        return self.init_pos == value
