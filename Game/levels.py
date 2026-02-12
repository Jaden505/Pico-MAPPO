from game.entities import Door, Key, Button
from game.entities.headless_rect import Rect


def get_levels():
    levels = []

    # Level 0 – Simple walk, open door jump over small block
    levels.append({
        "level_idx": 0,
        "static_obstacles": [Rect(0, 700, 2000, 100), Rect(1000, 600, 100, 100)],
        "coins": [Rect(950, 550, 30, 30), Rect(1050, 550, 30, 30)], # enourage jumping
        "door": Door((1800, 700), is_open=True),
        "key": None,
        "button": None
    })

    # Level 1 – Basic key pickup
    levels.append({
        "level_idx": 1,
        "static_obstacles": [Rect(-500, 700, 2500, 100)],
        # encourage collecting key first with coins near key 
        "coins": [Rect(750, 550, 30, 30), Rect(820, 620, 30, 30), Rect(900, 550, 30, 30)],
        "door": Door((1800, 700)),
        "key": Key((800, 450)),
        "button": None
    })

    # Level 2 – Platform jumps to key
    levels.append({
        "level_idx": 2,
        "static_obstacles": [
            Rect(0, 700, 2000, 100),
            Rect(600, 600, 120, 100),
            Rect(800, 520, 120, 100),
            Rect(1000, 420, 120, 100)
        ],
        "coins": [Rect(620, 550, 30, 30), Rect(820, 470, 30, 30), Rect(1020, 370, 30, 30)],
        "door": Door((1800, 700)),
        "key": Key((1040, 340)),
        "button": None
    })

    # Level 3 – Pit gap
    levels.append({
        "level_idx": 3,
        "static_obstacles": [
            Rect(0, 700, 700, 100),
            Rect(800, 700, 1800, 100)
        ],
        "coins": [Rect(200, 650, 30, 30), Rect(700, 650, 30, 30), Rect(1200, 650, 30, 30), 
                    Rect(900, 550, 30, 30), Rect(1000, 550, 30, 30)
                    ],
        "door": Door((2000, 700)),
        "key": Key((900, 450)),
        "button": None
    })

    # Level 4 – Staggered platforms
    levels.append({
        "level_idx": 4,
        "static_obstacles": [
            Rect(0, 700, 300, 100),
            Rect(400, 650, 300, 100),
            Rect(800, 600, 300, 100),
            Rect(1200, 700, 1000, 100)
        ],
        # Coins to encourage jumping on all platforms
        "coins": [Rect(250, 650, 30, 30),
                    Rect(450, 600, 30, 30), Rect(650, 600, 30, 30),
                    Rect(850, 550, 30, 30), Rect(1050, 550, 30, 30)
                    ],
        "door": Door((2000, 700)),
        "key": Key((850, 520)),
        "button": None
    })

    # Level 5 – Button raises bridge
    bridge = Rect(1000, 650, 200, 0)
    levels.append({
        "level_idx": 5,
        "static_obstacles": [
            Rect(-200, 700, 1100, 100),
            Rect(1200, 700, 1800, 100),
            bridge
        ],
        # Coins to encourage going to key and button first
        "coins": [
                    Rect(-50, 650, 30, 30), Rect(-70, 550, 30, 30),
                    Rect(900, 550, 30, 30), Rect(1080, 600, 30, 30),
                    Rect(1300, 650, 30, 30), Rect(1700, 650, 30, 30)
                    ],
        "door": Door((2900, 700)),
        "key": Key((-100, 450)),
        "button": Button((850, 700), bridge, mode='appear', appear_height=50)
    })

    # Level 6 – Multi-jump to key
    bridge = Rect(800, 700, 200, 0)
    levels.append({
        "level_idx": 6,
        "static_obstacles": [
            Rect(0, 700, 800, 100),
            Rect(1000, 650, 200, 100),
            bridge,
            Rect(1300, 600, 200, 100),
            Rect(1600, 700, 2000, 100)
        ],
        # Coins to encourage going stacking players for jump annd under key to stack
        "coins": [
                    Rect(900, 450, 30, 30), Rect(400, 650, 30, 30),
                    Rect(1050, 600, 30, 30), Rect(800, 500, 30, 30),
                    Rect(1350, 550, 30, 30), Rect(1650, 650, 30, 30),
                    Rect(1400, 420, 30, 30), Rect(1350, 450, 30, 30),
                    Rect(1480, 450, 30, 30)
                        ],
        "door": Door((2800, 700)),
        "key": Key((1400, 300)),
        "button": Button((1050, 650), bridge, mode='appear', appear_height=50)
    })

    # Level 7 – Button removes wall
    wall = Rect(1000, 500, 100, 200)
    levels.append({
        "level_idx": 7,
        "static_obstacles": [
            Rect(0, 700, 1000, 100),
            wall,
            Rect(500, 550, 100, 30),
            Rect(600, 450, 100, 30),
            Rect(1150, 700, 2000, 100)
        ],
        "coins": [
                    Rect(400, 550, 30, 30), Rect(1050, 550, 30, 30),
                    Rect(550, 500, 30, 30), Rect(650, 400, 30, 30),
                    Rect(1200, 650, 30, 30), Rect(1600, 650, 30, 30)
                    ],
        "door": Door((2800, 700)),
        "key": Key((700, 620)),
        "button": Button((650, 450), wall, mode='dissapear')
    })

    return levels
