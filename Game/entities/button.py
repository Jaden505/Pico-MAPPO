import pygame

class Button:
    def __init__(self, position, static_obstacle, appearence, appear_height=100):
        self.is_pressed = False
        self.static_obstacle = static_obstacle
        self.appearance = appearence
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
        if self.appearance == 'dissapear':
            self.static_obstacle.height = 0
        elif self.appearance == 'appear':
            self.static_obstacle.height = self.appear_height