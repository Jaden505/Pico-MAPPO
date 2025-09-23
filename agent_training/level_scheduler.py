import random

class LevelScheduler:
    def __init__(self, start):
        self.n_levels = 8
        self.levels_sample_length = 3 # Amount of levels to sample through at a time
        self.current_level = start
        
    def sample_levels(self):
        # Sample levels around the current level
        low = max(0, self.current_level - self.levels_sample_length // 2)
        high = min(self.n_levels, low + self.levels_sample_length)
        low = max(0, high - self.levels_sample_length) # Adjust low if at end of range
        return list(range(low, high))
    
