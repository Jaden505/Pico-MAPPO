import pygame
pygame.init()
pygame.display.set_caption('Pico Park')

from Game.env import Environment
from MAPPO.ppo import PPO

env = Environment(level_index=0)  # Initialize environment with level index 0
ppo = PPO(env)
    
states, actions, rewards = ppo.rollout()

print(f"Collected {len(states)} states, {len(actions)} actions, and {len(rewards)} rewards.")