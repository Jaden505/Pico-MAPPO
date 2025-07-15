import pygame

class Player:
    def __init__(self, init_pos):
        # Sprites
        self.stand_right = pygame.image.load('sprites/pico_stand.png')
        self.stand_left = pygame.transform.flip(self.stand_right, True, False)
        
        self.walk_right = [pygame.image.load(f'sprites/pico_move{i}.png') for i in range(1,5)]
        self.walk_left = [pygame.transform.flip(img, True, False) for img in self.walk_right]
        
        self.jump_right = pygame.image.load('sprites/pico_jump.png')
        self.jump_left = pygame.transform.flip(self.jump_right, True, False)
        
        self.sprite = self.stand_right
        
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        
        self.p_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Orientation
        self.facing_left = False
        self.jumping = False
        
        self.x, self.y = init_pos[0], init_pos[1]
        self.vx, self.vy = 0, 0
        self.acx, self.acy = 10000, 800
        
        self.jump_gravity = 40
        
        # Extras
        self.walk_cycle_ind = 0 # Which run sprite image to show in sequence
        self.push_cycle_ind = 0
        
        self.walk_cycle_len = len(self.walk_right)
        self.anim_timer = 0
        self.anim_speed = 0.15  # seconds per frame
        
        
    def update_sprite(self, dt):
        if self.vx == 0 and self.vy == 0 and not self.jumping:
            self.sprite = self.stand_left if self.facing_left else self.stand_right
        elif self.jumping:
            self.sprite = self.jump_left if self.facing_left else self.jump_right
        else:
            self.anim_timer += dt
            
            if self.anim_timer > self.anim_speed:
                self.sprite = self.walk_left[self.walk_cycle_ind] if self.facing_left else self.walk_right[self.walk_cycle_ind]
                self.walk_cycle_ind = self.walk_cycle_ind+1 if self.walk_cycle_ind < self.walk_cycle_len-1 else 0
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
        

    def move_and_collide(self, static_obstacles,  dt):     
        # Horizontal collision
        self.x += self.vx * dt 
        self.p_rect.x = self.x
        
        for obs in static_obstacles:
            if p_rect.colliderect(obs.rect): 
                if self.vx > 0: # hit right wall
                    self.x = obs.left - self.width

                elif self.vx < 0: # hit left wall
                    self.x = obs.right
                
                self.vx = 0
                    
        # Vertical collision     
        if self.vy < self.acy: # apply jump gravity
            self.vy += self.jump_gravity
            
        self.y += self.vy * dt
               
        self.p_rect.y = self.y
        for obs in static_obstacles:
            if p_rect.colliderect(obs.rect):   
                if self.vy > 0: # hit floor
                    self.y = obs.top - self.height 
                    self.jumping = False
                    
                elif self.vy < 0: # hit ceiling
                    self.y = obs.bottom
                    self.jumping = False
                    
                self.vy = 0