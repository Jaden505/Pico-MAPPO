from game.utils import load_sprite
from game.entities.headless_rect import Rect

class Door:
    def __init__(self, position, is_open=False):
        left, bottom = position
        self.is_open = is_open
        self.left = left
        width, height = 130, 130
        
        self.sprite_closed = load_sprite('door_closed.png')
        self.sprite_open = load_sprite('door_open.png')
        self.rect = Rect(left, bottom - height, width, height)

    def draw(self, screen, offset):
        if self.is_open:
            screen.blit(self.sprite_open, (self.rect.x - offset[0], self.rect.y - offset[1]))
        else:
            screen.blit(self.sprite_closed, (self.rect.x - offset[0], self.rect.y - offset[1]))

    def toggle(self):
        self.is_open = not self.is_open
        
    @property
    def positionxy(self):
        return [self.rect.x, self.rect.y]