
class PPO:
    def __init__(self, env):
        self.env = env
        self.state_dim = env.state_space.shape()
        self.action_dim = env.action_space.shape()
        
        self.init_hyperparams()
        
    def init_hyperparams(self):
        self.timesteps_per_batch = 100000 
        self.max_timesteps_per_episode = 5000
    
    def rollout(self):
        pass