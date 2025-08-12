from MAPPO.actorcritic import ActorCritic
import pygame
import time

class PPO:
    def __init__(self, env):
        self.env = env
        self.state_dim = env.state_space_shape
        self.action_dim = env.action_space_shape
        
        self.actor = ActorCritic(self.state_dim, self.action_dim)
        self.critic = ActorCritic(self.state_dim, 1)
        
        self.init_hyperparams()
        
    def init_hyperparams(self):
        self.timesteps_per_batch = 60000 
        self.max_timesteps_per_episode = 5000
           
    def rollout(self):
        states = []
        actions = []
        rewards = []
        
        t = 0
        
        pygame.display.update()

        # waint until user quits
        running = True
        while t < self.timesteps_per_batch and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                    
            self.env.reset(self.env.level_index)
            
            for ep_t in range(self.max_timesteps_per_episode):
                for agent in self.env.agents:
                
                    state = self.env.get_state()
                    action_logits = self.actor.forward(state)
                    action_probs = self.actor.softmax(action_logits)
                    action, reward, done = self.env.step(agent.id, action_probs)
                    
                    states.append(state)
                    actions.append(action_logits)
                    rewards.append(reward)
        
                if done:
                    break
                
                t += 1
        
        return states, actions, rewards
    
