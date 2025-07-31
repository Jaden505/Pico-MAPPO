from actorcritic import ActorCritic

class PPO:
    def __init__(self, env):
        self.env = env
        self.state_dim = env.state_space.shape()
        self.action_dim = env.action_space.shape()
        
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
        timesteps = []
        
        t = 0
        while t < self.timesteps_per_batch:
            self.env.reset(self.env.level_index)
            
            for agent in self.env.agents:
                for ep_t in range(self.max_timesteps_per_episode):
                    
                    state = self.env.get_state(agent.id)
                    action_probs = self.actor.forward(state)
                    action, reward, done = self.env.step(agent.id, action_probs)
                    
                    states.append(state)
                    actions.append(action)
                    rewards.append(reward)
                    timesteps.append(ep_t)
            
                    if done:
                        break
        
            t = len(timesteps)
                    
        return states, actions, rewards, timesteps
    
    
    