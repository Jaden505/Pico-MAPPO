from game.env import GameEnv
from agent_training.ppo import PPO
from agent_training.level_scheduler import LevelScheduler
from game.levels import get_levels

import pygame

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Pico Park')
pygame.display.set_mode((1200, 800))

# Config
MAX_THREADS = 5
N_ITERATIONS = 100
N_TRAIN_EPISODES = 10
levels = get_levels()

ppo = PPO()
scheduler = LevelScheduler(levels, start_idx=0)

envs = [GameEnv(level=scheduler.sample_level(), visualize=False) for i in range(MAX_THREADS)] # Visualize only last env
    
for _ in range(N_ITERATIONS):
    print(f"Starting iteration {_+1}/{N_ITERATIONS}")
    states, actions, action_logs, rewards_to_go, completed_levels = ppo.collect_batch_data(envs, scheduler)
    
    for _ in range(N_TRAIN_EPISODES):
        ppo.learn_actor_critic(states, actions, rewards_to_go, action_logs)
    
    # Record results and reset environments
    for level_idx, success in completed_levels:
        scheduler.record_result(level_idx, success)

pygame.quit()
