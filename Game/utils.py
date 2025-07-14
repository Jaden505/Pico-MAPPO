import pygame

def check_if_on_ground(player, grounds, sprite_width, sprite_height):
    player_rect = pygame.Rect(player.x, player.y, sprite_width, sprite_height+1)
    
    for g in grounds:
        if player_rect.colliderect(g) and player.vy >= 0:
            player.y = g.top - sprite_height+1
            player.vy = 0
            player.jumping = False
            return True
    return False