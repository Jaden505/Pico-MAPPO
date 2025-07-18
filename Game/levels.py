import pygame
from entities.door import Door
from entities.key import Key
from entities.button import Button

def get_levels():
    return [
        {
            "static_obstacles": [
                pygame.Rect(0, 700, 2000, 100)
            ],
            "door": Door((1800, 700), is_open=True),
            "key": None,
            "button": None
        },
        {
            "static_obstacles": [
                pygame.Rect(0, 700, 2000, 100),
                pygame.Rect(600, 600, 100, 100)
            ],
            "door": Door((1800, 700), is_open=True),
            "key": None,
            "button": None
        },
        {
            "static_obstacles": [
                pygame.Rect(0, 700, 2000, 100),
                pygame.Rect(900, 600, 100, 100),
                pygame.Rect(1200, 500, 100, 200)
            ],
            "door": Door((1800, 700)),
            "key": Key((600, 620)),
            "button": None
        },
        {
            "static_obstacles": [
                pygame.Rect(0, 700, 500, 100),
                pygame.Rect(700, 700, 1500, 100)
            ],
            "door": Door((2000, 700)),
            "key": Key((900, 620)),
            "button": None
        },
        {
            "static_obstacles": [
                pygame.Rect(0, 700, 300, 100),
                pygame.Rect(400, 650, 300, 100),
                pygame.Rect(800, 600, 300, 100),
                pygame.Rect(1200, 700, 1000, 100)
            ],
            "door": Door((2000, 700)),
            "key": Key((850, 520)),
            "button": None
        },
        {
            "static_obstacles": [
                pygame.Rect(0, 700, 900, 100),
                pygame.Rect(1200, 700, 1800, 100),
                pygame.Rect(1000, 650, 200, 0)
            ],
            "door": Door((2900, 700)),
            "key": Key((300, 620)),
            "button": Button((950, 700), pygame.Rect(1000, 650, 200, 0), 'appear', appear_height=50)
        },
        {
            "static_obstacles": [
                pygame.Rect(0, 700, 300, 100),
                pygame.Rect(500, 650, 200, 100),
                pygame.Rect(800, 600, 200, 100),
                pygame.Rect(1100, 700, 2000, 100)
            ],
            "door": Door((2800, 700)),
            "key": Key((900, 520)),
            "button": None
        },
        {
            "static_obstacles": [
                pygame.Rect(0, 700, 1000, 100),
                pygame.Rect(1000, 500, 100, 200),
                pygame.Rect(1200, 700, 2000, 100)
            ],
            "door": Door((2800, 700)),
            "key": Key((200, 620)),
            "button": Button((950, 700), pygame.Rect(1000, 500, 100, 200), 'dissapear')
        },
        {
            "static_obstacles": [
                pygame.Rect(0, 700, 700, 100),
                pygame.Rect(900, 500, 100, 300),
                pygame.Rect(1200, 700, 2000, 100)
            ],
            "door": Door((2900, 700)),
            "key": Key((950, 420)),
            "button": None
        },
        {
            "static_obstacles": [
                pygame.Rect(0, 700, 700, 100),
                pygame.Rect(800, 500, 100, 200),
                pygame.Rect(1000, 700, 100, 100),
                pygame.Rect(1200, 650, 300, 0),
                pygame.Rect(1600, 700, 2000, 100)
            ],
            "door": Door((3500, 700)),
            "key": Key((300, 620)),
            "button": Button((950, 700), pygame.Rect(1200, 650, 300, 0), 'appear', appear_height=50)
        }
    ]
