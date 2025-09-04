from MAPPO.actorcritic import ActorCritic
from MAPPO.utils.math import softmax_log_probilities

from torch.optim import Adam
import torch
import pygame
import numpy as np

class PPO:
    def __init__(self, env):
        self.init_hyperparams()
        self.env = env
        self.state_dim = env.state_space_shape
        self.action_dim = env.action_space_shape
        
        self.actor = ActorCritic(self.state_dim, self.action_dim)
        self.critic = ActorCritic(self.state_dim, 1)
        
        self.actor_optim = Adam(self.actor.parameters(), lr=self.lr)
        self.critic_optim = Adam(self.critic.parameters(), lr=self.lr)
        
        
    def init_hyperparams(self):
        self.timesteps_per_batch = 20
        self.max_timesteps_per_episode = 10
        self.n_updates_per_iteration = self.timesteps_per_batch // self.max_timesteps_per_episode
        self.clip = 0.2
        self.lr = 0.0005
        
           
    def rollout(self):
        states = []
        actions = []
        action_log_probs = []
        rewards = []
        rewards_to_go = []
        batch_lens = []        
        
        t = 0
        while t < self.timesteps_per_batch:
            if 'completed' in self.env.level: # Go to next level if current level is completed
                self.env.level_index += 1
                
            self.env.reset(self.env.level_index)
            done = False
            
            for ep_t in range(min(self.timesteps_per_batch - t, self.max_timesteps_per_episode)):
                for agent in self.env.agents:
                    state = self.env.get_state()
                    action_logits = self.actor.forward(state)
                    soft_log_probs = softmax_log_probilities(action_logits)
                    action, reward, done = self.env.step(agent.id, soft_log_probs)
                    
                    states.append(state)
                    actions.append(action)
                    action_log_probs.append(soft_log_probs)
                    rewards.append(reward)
                    
                    if done:
                        break
                
                if done:
                    break
                    
            t += (ep_t + 1)
            rewards_to_go += [sum(rewards[i:]) for i in range(len(rewards))]
                                
            batch_lens.append(ep_t + 1)
        
        return states, actions, action_log_probs, rewards, rewards_to_go, batch_lens
    

    def learn(self):
        for _ in range(self.n_updates_per_iteration):
            states, actions, action_log_probs, rewards, rewards_to_go, batch_lens = self.rollout()
            states = np.array(states)
            rewards_to_go = torch.tensor(rewards_to_go).float()
            
            V = self.critic.forward(states).squeeze() # V is the value function which represents what the critic thinks the expected reward is
            print(len(states), len(rewards_to_go), V.shape)
            A_raw = rewards_to_go - V.detach()
            norm_A = (A_raw - A_raw.mean()) / (A_raw.std() + 1e-10)
            A = torch.tensor(norm_A).float() # Advantage function is the difference between the expected reward and the actual reward
            
            curr_action_log = self.actor.forward(states)
            curr_log_probs = softmax_log_probilities(curr_action_log)
            
            ratios = torch.exp(curr_log_probs - torch.tensor(action_log_probs).float())
            surr1 = ratios * A
            surr2 = torch.clamp(ratios, 1 - self.clip, 1 + self.clip) * A
            actor_loss = (-torch.min(surr1, surr2)).mean()
            
            # Backpropagation for actor network
            self.actor_optim.zero_grad() # reset gradients
            actor_loss.backward()
            self.actor_optim.step() # update actor network weights

            # Critic loss
            critic_loss = torch.nn.MSELoss()(V, torch.tensor(rewards_to_go).float())
            self.critic_optim.zero_grad()
            critic_loss.backward()
            self.critic_optim.step()
            