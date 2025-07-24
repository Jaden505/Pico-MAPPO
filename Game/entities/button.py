import pygame

class Button:
    def __init__(self, position, static_obstacle, mode='appear', appear_height=100):
        self.is_pressed = False
        self.static_obstacle = static_obstacle
        self.mode = mode
        self.appear_height = appear_height
        
        left, bottom = position
        width, height = 50, 50
        
        bottom += 20 # Adjust button position slightly in the ground
        
        def load_sprite(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (width, height))
        
        self.button = load_sprite('sprites/button.png')
        self.button_pressed = load_sprite('sprites/button_pressed.png')
        self.rect = pygame.Rect(left, bottom - height, width, height)

    def draw(self, screen, offset):
        if self.is_pressed:
            screen.blit(self.button_pressed, (self.rect.x - offset[0], self.rect.y - offset[1]))
        else:
            screen.blit(self.button, (self.rect.x - offset[0], self.rect.y - offset[1]))

    def toggle(self):
        self.is_pressed = True
        if self.mode == 'dissapear':
            self.static_obstacle.height = 0
        elif self.mode == 'appear':
            self.static_obstacle.height = self.appear_height
            
    @property
    def get_position_on_screen(self, xmin, xmax):
        if self.is_pressed or self.rect.x < xmin or self.rect.x > xmax:
                return [0, 0]
        else:
            return [self.rect.x, self.rect.y]