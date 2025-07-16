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
