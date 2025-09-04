from Game.env import Environment
from MAPPO.ppo import PPO

import pygame

pygame.init()
pygame.display.set_caption('Pico Park')

env = Environment(level_index=0)  # Initialize environment with level index 0
ppo = PPO(env)
    
ppo.learn()
pygame.quit()