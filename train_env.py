from Game.env import Environment
from MAPPO.ppo import PPO

import pygame

pygame.init()
pygame.display.set_caption('Pico Park')

ppo = PPO()
    
ppo.learn()
pygame.quit()