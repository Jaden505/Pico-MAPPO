from game.env import Environment
from agent_training.ppo import PPO

import pygame

pygame.init()
pygame.display.set_caption('Pico Park')

ppo = PPO()
    
ppo.learn()
pygame.quit()