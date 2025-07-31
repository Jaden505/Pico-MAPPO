import pygame

class Key:
    def __init__(self, position):
        self.position = position
        width, height = 65, 80
        
        self.sprite = pygame.image.load('sprites/key.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.holder = None  # To track which player holds the key
        self.used = False

    def draw(self, screen, offset, dt):
        if self.used:
            return
        
        if self.holder:
            # If a player holds the key, slowly move it to their position above their head
            holder_x = self.holder.x + (self.holder.width - self.rect.width) // 2
            holder_y = self.holder.y - self.rect.height
            move_x = holder_x - self.rect.x
            move_y = holder_y - self.rect.y
            self.rect.x += move_x * dt  # Smoothly move towards the holder's position
            self.rect.y += move_y * dt
            screen.blit(self.sprite, (self.rect.x - offset[0], self.rect.y - offset[1]))
        else:
            screen.blit(self.sprite, (self.rect.x - offset[0], self.rect.y - offset[1]))

    def collect(self, player):
        self.holder = player
        player.has_key = True
        
    @property
    def positionxy(self, xmin, xmax):
        if self.holder or self.used or self.rect.x < xmin or self.rect.x > xmax:
                return [0, 0]
        else:
            return [self.rect.x, self.rect.y]