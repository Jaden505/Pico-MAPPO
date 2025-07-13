import pygame

class Player:
    def __init__(self, init_pos, dt):
        self.sprite_right = pygame.image.load('sprites/pico-stand.png')
        self.sprite_left = pygame.transform.flip(self.sprite_right, True, False)
        self.sprite = self.sprite_right
        
        self.dt = dt
        self.orientation = [False, False]
        self.jumping = False
        
        self.x, self.y = init_pos[0], init_pos[1]
        self.vx, self.vy = 0, 0
        self.acx, self.acy = 100, 100
        
        self.move_cycle_ind = 0
        self.push_cycle_ind = 0
        
    def update_sprite():
        img_move_cycle = ['pico_push1.png', 'pico_push2.png', 'pico_push3.png', 'pico_push4.png']
        
    def set_controls(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.orientation[0] = True
                self.sprite = self.sprite_left
            elif event.key == pygame.K_RIGHT:
                self.orientation[1] = True
                self.sprite = self.sprite_right
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.orientation[0] = False
            elif event.key == pygame.K_RIGHT:
                self.orientation[1] = False
        
    def move_controls(self):     
        if self.orientation[0]:
            self.vx = -self.acx * self.dt
        elif self.orientation[1]:
            self.vx = self.acx * self.dt
        else:
            self.vx = 0
                
        self.x += self.vx * self.dt
            