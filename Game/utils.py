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

def find_mutual_xcenter(player_agents):
    """Find the mutual x center of all player agents."""
    if not player_agents:
        return 0

    min_x = min(agent.x for agent in player_agents)
    max_x = max(agent.x + agent.width for agent in player_agents)
    return (min_x + max_x) // 2

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
        if obj[1] > xmin_limit and obj[0] < xmax_limit:  # Only include objects within the screen limits
            clipped_obj = [
                normalize_xposition(obj[0], xmin_limit, xmax_limit),
                normalize_xposition(obj[1], xmin_limit, xmax_limit),
                normalize_yposition(obj[2], screen_height),
                normalize_yposition(obj[3], screen_height)
            ]
            normalized.append(clipped_obj)
    return normalized

def normalize_state_agents(state_agents, xmin_limit, xmax_limit, screen_height):
    normalized = []
    for agent in state_agents:
        if xmin_limit <= agent[1] <= xmax_limit:  # Only include agents within the screen limits
            normalized_agent = [
                agent[0],  # id
                normalize_xposition(agent[1], xmin_limit, xmax_limit),
                normalize_yposition(agent[2], screen_height),
                agent[3],  # vx
                agent[4],  # vy
                1 if agent[5] else 0,  # is_jumping
                1 if agent[6] else 0   # has_key
            ]
            normalized.append(normalized_agent)
    return normalized

def normalize_state_interactables(state_interactables, xmin_limit, xmax_limit, screen_height):
    normalized = []
    for interactable in state_interactables:
        if xmin_limit <= interactable[0] <= xmax_limit:  # Only include interactables within the screen limits
            normalized_interactable = [
                normalize_xposition(interactable[0], xmin_limit, xmax_limit),
                normalize_yposition(interactable[1], screen_height),
                1 if interactable[2] else 0  # is_open or is_pressed
            ]
            normalized.append(normalized_interactable)
    return normalized