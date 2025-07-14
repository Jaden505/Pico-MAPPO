import pygame

class Player:
    def __init__(self, init_pos, dt):
        # Sprites
        self.stand_right = pygame.image.load('sprites/pico_stand.png')
        self.stand_left = pygame.transform.flip(self.stand_right, True, False)
        
        self.walk_right = [pygame.image.load(f'sprites/pico_move{i}.png') for i in range(1,5)]
        self.walk_left = [pygame.transform.flip(img, True, False) for img in self.walk_right]
        
        self.jump_right = pygame.image.load('sprites/pico_jump.png')
        self.jump_left = pygame.transform.flip(self.jump_right, True, False)
        
        self.sprite = self.stand_right
        
        self.dt = dt
        self.moving = [False, False]
        self.facing_left = False
        self.jumping = False
        
        self.x, self.y = init_pos[0], init_pos[1]
        self.vx, self.vy = 0, 0
        self.acx, self.acy = 200, 150
        
        self.jump_gravity = 8
        
        self.walk_cycle_ind = 0
        self.push_cycle_ind = 0
        
        self.walk_cycle_len = len(self.walk_right)
        self.anim_timer = 0
        self.anim_speed = 0.6  # seconds per frame
        
    def update_sprite(self):
        if not any(self.moving) and not self.jumping:
            self.sprite = self.stand_left if self.facing_left else self.stand_right
        elif self.jumping:
            self.sprite = self.jump_left if self.facing_left else self.jump_right
        else:
            self.anim_timer += self.dt
            
            if self.anim_timer > self.anim_speed:
                self.sprite = self.walk_left[self.walk_cycle_ind] if self.facing_left else self.walk_right[self.walk_cycle_ind]
                self.walk_cycle_ind = self.walk_cycle_ind+1 if self.walk_cycle_ind < self.walk_cycle_len-1 else 0
                self.anim_timer = 0
        
        
    def set_controls(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving[0] = True
                self.facing_left = True
            elif event.key == pygame.K_RIGHT:
                self.moving[1] = True
                self.facing_left = False
            elif event.key == pygame.K_SPACE and not self.jumping:
                self.jumping = True
                self.vy = -self.acy
                self.move_controls(False)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving[0] = False
            elif event.key == pygame.K_RIGHT:
                self.moving[1] = False

        
    def move_controls(self, touching_ground):     
        if self.moving[0]:
            self.vx = -self.acx * self.dt
        elif self.moving[1]:
            self.vx = self.acx * self.dt
        else:
            self.vx = 0
                        
        if touching_ground:
            self.vy = 0
            self.jumping = False
        else:
            self.vy += self.jump_gravity
                
        self.x += self.vx * self.dt
        self.y += self.vy * self.dt
            