from game.env import GameEnv
from agent_training.ppo import PPO
from agent_training.level_scheduler import LevelScheduler
from game.levels import levels

import pygame

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Pico Park')

# Config
MAX_THREADS = 6
N_ITERATIONS = 100

ppo = PPO()
scheduler = LevelScheduler(levels, start=0)
envs = [GameEnv(level=scheduler.sample_level(), visualize=(i==MAX_THREADS-1)) for i in range(MAX_THREADS)] # Visualize only last env
    
for _ in range(N_ITERATIONS):
    print(f"Starting iteration {_+1}/{N_ITERATIONS}")
    states, action_logs, rewards_to_go, completions = ppo.collect_batch_data(envs, scheduler)
    ppo.learn_actor_critic(states, rewards_to_go, action_logs)
    
    # Record results and reset environments
    for i, env in enumerate(envs):
        scheduler.record_result(env.level, completions[i])
        env.reset(scheduler.sample_level())

pygame.quit()