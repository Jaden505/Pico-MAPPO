import pygame

PLAYER_COLOR_MAPS = {
    'green': {
        (127, 191, 255): (166, 255, 167), # light
        (38, 142, 236): (118, 179, 118), # dark
    },
    'red': {
        (127, 191, 255): (255, 140, 140), # light
        (38, 142, 236): (179, 98, 98), # dark 
    },
    'yellow': {
        (127, 191, 255): (255, 255, 140), # light
        (38, 142, 236): (179, 179, 98), # dark 
    }
}

def recolor_image(surface, color_map):
    surface = surface.copy()
    pxarray = pygame.PixelArray(surface)
    for old, new in color_map.items():
        pxarray.replace(surface.map_rgb(old), surface.map_rgb(new))
    del pxarray
    return surface

def find_mutual_xcenter(player, agents):
    total_x = player.x + sum(a.x for a in agents)
    count = 1 + len(agents)
    return total_x // count

def event_to_action(event, vx):
    """Helper function to convert pygame events to player actions."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT: return 'left'
        if event.key == pygame.K_RIGHT: return 'right'
        if event.key == pygame.K_SPACE: return 'jump'
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT and vx < 0: return 'stand'
        if event.key == pygame.K_RIGHT and vx > 0: return 'stand'
    return None
