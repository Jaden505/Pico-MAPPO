from MAPPO.actorcritic import ActorCritic

from torch.optim import Adam
import torch
import torch.nn.functional as F
import numpy as np
from torch.distributions import Categorical

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
        self.timesteps_per_batch = 6000
        self.max_timesteps_per_episode = 600
        self.n_updates_per_iteration = self.timesteps_per_batch // self.max_timesteps_per_episode
        self.clip = 0.2
        self.lr = 0.005
        self.gamma = 0.98
        
    def calculate_rtgs(self, ep_rewards):
        G = 0
        rewards_to_go = []
        for r in reversed(ep_rewards):
            G = r + self.gamma * G
            rewards_to_go.insert(0, G) 
            
        return rewards_to_go
           
    def rollout(self):
        states = []
        action_logs = []
        rewards = []
        rewards_to_go = []
        batch_lens = []        
        
        t = 0
        while t < self.timesteps_per_batch:
            if 'completed' in self.env.level: # Go to next level if current level is completed
                self.env.level_index += 1
                
            self.env.reset(self.env.level_index)
            
            done = False
            ep_t = 0
            ep_rewards = []
            
            while ep_t < self.max_timesteps_per_episode and ep_t < (self.timesteps_per_batch - t) and not done:
                for agent in self.env.agents:
                    state = self.env.get_state()
                    
                    action_logits = self.actor.forward(state)
                    action_prob = F.softmax(action_logits, dim=-1)
                    action, reward, done = self.env.step(agent.id, action_prob.detach().numpy())
                    action_log = F.log_softmax(action_logits, dim=-1)[action]
                    
                    states.append(state)
                    action_logs.append(action_log.float())
                    ep_rewards.append(reward)
                    ep_t += 1

            t += (ep_t + 1)
            batch_lens.append(ep_t + 1)
            rewards.append(ep_rewards)
            rewards_to_go.extend(self.calculate_rtgs(ep_rewards))

        return np.array(states), torch.tensor(action_logs), rewards, torch.tensor(rewards_to_go).float(), batch_lens
    

    def learn(self):
        for _ in range(self.n_updates_per_iteration):
            states, action_logs, rewards, rewards_to_go, batch_lens = self.rollout()
            
            # Calculate advantage
            V = self.critic.forward(states).squeeze() # Critic state value
            A_raw = rewards_to_go - V.detach()
            norm_A = (A_raw - A_raw.mean()) / (A_raw.std() + 1e-10) # Normalize advantage
            A = norm_A.clone() # Advantage estimation
            
            curr_action = self.actor.forward(states)
            curr_probs = Categorical(logits=curr_action)
            curr_action = curr_probs.sample()
            curr_logs = curr_probs.log_prob(curr_action)
            
            ratios = torch.exp(curr_logs - action_logs)
            surr1 = ratios * A 
            surr2 = torch.clamp(ratios, 1 - self.clip, 1 + self.clip) * A
            actor_loss = (-torch.min(surr1, surr2)).mean()
            
            # Backpropagation for actor network
            self.actor_optim.zero_grad() # reset gradients 
            actor_loss.backward()
            self.actor_optim.step() # update actor network weights

            # Critic loss
            critic_loss = torch.nn.MSELoss()(V, rewards_to_go)
            self.critic_optim.zero_grad()
            critic_loss.backward()
            self.critic_optim.step()
            