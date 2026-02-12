from game.utils import load_sprite
from game.entities.headless_rect import Rect

class Button:
    def __init__(self, position, static_obstacle, mode='appear', appear_height=100):
        self.is_pressed = False
        self.static_obstacle = static_obstacle
        self.mode = mode
        self.appear_height = appear_height
        
        left, bottom = position
        width, height = 50, 50
        
        bottom += 20 # Adjust button position slightly in the ground
        
        self.button = load_sprite('button.png', (width, height))
        self.button_pressed = load_sprite('button_pressed.png', (width, height))
        self.rect = Rect(left, bottom - height, width, height)

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
    def positionxy(self):
        return [self.rect.x, self.rect.y]