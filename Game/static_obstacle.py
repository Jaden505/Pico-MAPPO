import pygame

class StaticObstacle:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        
        self.rect = pygame.Rect(left, top, width, height)
        
    @property
    def right(self):
        return self.left + self.width
    
    @property
    def bottom(self):
        return self.top - self.height
    
    @property
    def coords(self):
        return [self.left, self.top, self.width, self.height]
