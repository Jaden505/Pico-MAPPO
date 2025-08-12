import pygame
from Game.entities.door import Door
from Game.entities.key import Key
from Game.entities.button import Button

def get_levels():
    levels = []

    # Level 0 – Simple walk, open door
    levels.append({
        "static_obstacles": [pygame.Rect(0, 700, 2000, 100), pygame.Rect(1000, 600, 100, 100)],
        "door": Door((1800, 700), is_open=True),
        "key": None,
        "button": None
    })

    # Level 1 – Basic key pickup
    levels.append({
        "static_obstacles": [pygame.Rect(-500, 700, 2500, 100)],
        "door": Door((1800, 700)),
        "key": Key((300, 500)),
        "button": None
    })

    # Level 2 – Platform jumps to key
    levels.append({
        "static_obstacles": [
            pygame.Rect(0, 700, 2000, 100),
            pygame.Rect(600, 600, 120, 100),
            pygame.Rect(800, 520, 120, 100),
            pygame.Rect(1000, 420, 120, 100)
        ],
        "door": Door((1800, 700)),
        "key": Key((1040, 340)),
        "button": None
    })

    # Level 3 – Pit gap
    levels.append({
        "static_obstacles": [
            pygame.Rect(0, 700, 500, 100),
            pygame.Rect(600, 700, 1500, 100)
        ],
        "door": Door((2000, 700)),
        "key": Key((900, 620)),
        "button": None
    })

    # Level 4 – Staggered platforms
    levels.append({
        "static_obstacles": [
            pygame.Rect(0, 700, 300, 100),
            pygame.Rect(400, 650, 300, 100),
            pygame.Rect(800, 600, 300, 100),
            pygame.Rect(1200, 700, 1000, 100)
        ],
        "door": Door((2000, 700)),
        "key": Key((850, 520)),
        "button": None
    })

    # Level 5 – Button raises bridge
    bridge = pygame.Rect(1000, 650, 200, 0)
    levels.append({
        "static_obstacles": [
            pygame.Rect(0, 700, 900, 100),
            pygame.Rect(1200, 700, 1800, 100),
            bridge
        ],
        "door": Door((2900, 700)),
        "key": Key((2000, 620)),
        "button": Button((850, 700), bridge, mode='appear', appear_height=50)
    })

    # Level 6 – Multi-jump to key
    bridge = pygame.Rect(300, 700, 200, 0)
    levels.append({
        "static_obstacles": [
            pygame.Rect(0, 700, 300, 100),
            pygame.Rect(500, 650, 200, 100),
            bridge,
            pygame.Rect(800, 600, 200, 100),
            pygame.Rect(1100, 700, 2000, 100)
        ],
        "door": Door((2800, 700)),
        "key": Key((1400, 300)),
        "button": Button((650, 650), bridge, mode='appear', appear_height=50)
    })

    # Level 7 – Button removes wall
    wall = pygame.Rect(1000, 500, 100, 200)
    levels.append({
        "static_obstacles": [
            pygame.Rect(0, 700, 1000, 100),
            wall,
            pygame.Rect(500, 550, 100, 30),
            pygame.Rect(600, 450, 100, 30),
            pygame.Rect(1150, 700, 2000, 100)
        ],
        "door": Door((2800, 700)),
        "key": Key((700, 620)),
        "button": Button((650, 450), wall, mode='dissapear')
    })

    return levels
