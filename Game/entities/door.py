import pygame

class Door:
    def __init__(self, position, is_open=False):
        left, bottom = position
        self.is_open = is_open
        self.left = left
        width, height = 130, 130
        
        def load_sprite(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (width, height))
        
        self.sprite_closed = load_sprite('Game/sprites/door_closed.png')
        self.sprite_open = load_sprite('Game/sprites/door_open.png')
        self.rect = pygame.Rect(left, bottom - height, width, height)

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