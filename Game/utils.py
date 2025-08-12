import pygame
import numpy as np

PLAYER_COLOR_MAPS = {
    'green': {
        'id': 2,
        (127, 191, 255): (166, 255, 167), # light
        (38, 142, 236): (118, 179, 118), # dark
    },
    'red': {
        'id': 3,
        (127, 191, 255): (255, 140, 140), # light
        (38, 142, 236): (179, 98, 98), # dark 
    },
    'yellow': {
        'id': 4,
        (127, 191, 255): (255, 255, 140), # light
        (38, 142, 236): (179, 179, 98), # dark 
    }
}

def recolor_image(surface, color_map):
    surface = surface.copy()
    pxarray = pygame.PixelArray(surface)
    for old, new in color_map.items():
        if old == 'id':
            continue
        pxarray.replace(surface.map_rgb(old), surface.map_rgb(new))
    del pxarray
    return surface

def find_outer_x_limits(player_agents, screen_width, sprite_width=80):
    """Find the mutual x center of all player agents."""
    if not player_agents:
        return 0

    # first find mutual x center
    x_positions = [a.x for a in player_agents]
    
    # find mutual center of positions
    avg_pos = sum(x_positions) / len(x_positions)
    xmin_limit = avg_pos - screen_width / 2 + (sprite_width / 2)
    xmax_limit = avg_pos + screen_width / 2 - (sprite_width / 2)

    return xmin_limit, xmax_limit
    
    
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


def normalize_xposition(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin) 
    
def normalize_yposition(y, screen_height):
    return y / screen_height 

def normalize_state_obstacles(state_obstacles, xmin_limit, xmax_limit, screen_height):
    normalized = []
    for obj in state_obstacles:
        norm_obj = [
            normalize_xposition(obj[0], xmin_limit, xmax_limit),
            normalize_xposition(obj[1], xmin_limit, xmax_limit),
            normalize_yposition(obj[2], screen_height),
            normalize_yposition(obj[3], screen_height)
        ]
        normalized.append(norm_obj)
    return np.array(normalized).flatten()

def normalize_state_agents(state_agents, xmin_limit, xmax_limit, screen_height):
    normalized = []
    for agent in state_agents:
        norm_agent = [
            agent[0],  # id
            normalize_xposition(agent[1], xmin_limit, xmax_limit),
            normalize_yposition(agent[2], screen_height),
            agent[3],  # vx
            agent[4],  # vy
            1 if agent[5] else 0,  # is_jumping
            1 if agent[6] else 0   # has_key
        ]
        normalized.append(norm_agent)
    return np.array(normalized).flatten()

def normalize_state_interactables(state_interactables, xmin_limit, xmax_limit, screen_height):
    normalized = []
    for interactable in state_interactables:
        norm_interactable = [
            normalize_xposition(interactable[0], xmin_limit, xmax_limit),
            normalize_yposition(interactable[1], screen_height),
            1 if interactable[2] else 0  # is_open or is_pressed
        ]
        normalized.append(norm_interactable)
    return np.array(normalized).flatten()
