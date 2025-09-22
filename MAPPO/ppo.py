from MAPPO.actorcritic import ActorCritic
from Game.env import Environment

from torch.optim import Adam
import torch
import torch.nn.functional as F
import numpy as np
from torch.distributions import Categorical
import threading

class PPO:
    def __init__(self):
        env = Environment(level_index=0, visualize=True)
        self.highest_level = env.level_index
        
        self.init_hyperparams()
        self.state_dim = env.state_space_shape
        self.action_dim = env.action_space_shape
        
        self.actor = ActorCritic(self.state_dim, self.action_dim)
        self.critic = ActorCritic(self.state_dim, 1)
        
        self.actor_optim = Adam(self.actor.parameters(), lr=self.lr)
        self.critic_optim = Adam(self.critic.parameters(), lr=self.lr)
        
        
    def init_hyperparams(self):
        self.timesteps_per_batch = 400
        self.max_timesteps_per_episode = 70
        self.n_iterations = 100
        self.clip = 0.2
        self.lr = 0.005
        self.gamma = 0.98
        self.max_threads = 5
        
    def calculate_rtgs(self, ep_rewards):
        G = 0
        rewards_to_go = []
        for r in reversed(ep_rewards):
            G = r + self.gamma * G
            rewards_to_go.insert(0, G) 
            
        return rewards_to_go
    
    def gather_experience(self, env, return_dict, thread_id):
        ep_rewards = []
        ep_states = []
        ep_action_logs = []

        env.reset(self.highest_level)
        state = env.get_state()
        done = False
        
        for ep_t in range(self.max_timesteps_per_episode):
            for agent_id in (a.id for a in env.agents):
                with torch.no_grad():
                    action_logits = self.actor.forward(state)

                action_probs = Categorical(logits=action_logits)
                action = action_probs.sample()
                action_log = action_probs.log_prob(action)
                
                next_state, reward, done = env.step(agent_id, action.item())
                
                ep_states.append(state)
                ep_action_logs.append(action_log)
                ep_rewards.append(reward)
                
                state = next_state
                
                if done:
                    break
            
        return_dict[thread_id] = (ep_states, ep_action_logs, ep_rewards)
            
           
    def rollout(self):
        envs = [Environment(level_index=self.highest_level, visualize=(i==self.max_threads-1)) for i in range(self.max_threads)]
        
        states = []
        action_logs = []
        rewards = []
        rewards_to_go = []
        batch_lens = []       
        
        t = 0
        
        # create n threads to collect experience
        while t < self.timesteps_per_batch:
            threads = []
            return_dict = {}
            
            n_live_threads = min(self.max_threads, (self.timesteps_per_batch - t) // self.max_timesteps_per_episode + 1)
            for i in range(n_live_threads-1):
                thread = threading.Thread(target=self.gather_experience, args=(envs[i], return_dict, i))
                threads.append(thread)
                thread.start()
                
            # Run a batch on the main thread with visualization for debugging
            self.gather_experience(envs[-1], return_dict, n_live_threads)
            threads.append(None)  # Placeholder for main thread
            
            for i, thread in enumerate(threads):
                if thread: 
                    thread.join()
                    ep_states, ep_action_logs, ep_rewards = return_dict[i]
                else:
                    ep_states, ep_action_logs, ep_rewards = return_dict[n_live_threads]
                
                states.extend(ep_states)
                action_logs.extend(ep_action_logs)
                rewards.extend(ep_rewards)
                rewards_to_go.extend(self.calculate_rtgs(ep_rewards))
                batch_lens.append(len(ep_rewards))
                
                t += len(ep_rewards)
                
                if t >= self.timesteps_per_batch:
                    break
                
            print(f"Collected {t} timesteps")

        return np.array(states), torch.tensor(action_logs), rewards, torch.tensor(rewards_to_go).float(), batch_lens
    

    def learn(self):
        for _ in range(self.n_iterations):
            print(f"Starting iteration {_+1}/{self.n_iterations}")
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
            