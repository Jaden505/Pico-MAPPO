# A schedular to gradually increase levels and their difficulty while 20% repeating recent episodes and 10% older episode to prevent forgetting

from collections import deque
import numpy as np

class LevelScheduler:
    def __init__(self, levels, start_idx=0):
        self.levels = levels
        self.current_level = levels[start_idx]
        self.level_idx = start_idx
        
        self.n_recent_levels = 2 # Number of recent levels to sample from
        self.success_rate_window = 12 # Number of episodes to consider for success rate
        self.success_rate_threshold = 0.8 # Success rate threshold to level up
        self.recent_results = deque(maxlen=self.success_rate_window) # Store recent episode results (1 for success, 0 for fail)
        
    def sample_level(self):
        probs = np.zeros(len(self.levels))
        probs[self.level_idx] = (0.7 if self.level_idx > 0 else 1.0) # 70% chance to sample current level (100% if first level)

        for i in range(self.level_idx, 0, -1):
            if self.level_idx - i < self.n_recent_levels:
                if self.level_idx <= self.n_recent_levels:
                    probs[i] += 0.3 / self.n_recent_levels  # Distribute 30% chance among recent levels if no older levels 
                else:
                    probs[i] += 0.2 / self.n_recent_levels # 20% chance to sample recent levels
            else:
                probs[i] += 0.1 / (self.level_idx - self.n_recent_levels) # 10% chance to sample older levels
                
        return np.random.choice(self.levels, p=probs)
    
    def advance_level(self):
        if self.current_level < self.n_levels - 1:
            self.level_idx += 1
            self.current_level = self.levels[self.level_idx]
            self.recent_results.clear() 
            print(f"Level up! Moving to level {self.level_idx}")
            return True
        else:
            print("Already at highest level.")
            return False
        
    def record_result(self, level_idx, success):
        if level_idx == self.level_idx:
            self.recent_results.append(1 if success else 0) # Record only if the level matches current level
        
        if success:
            succes_rate = sum(self.recent_results) / len(self.recent_results)
            if len(self.recent_results) == self.success_rate_window and succes_rate >= self.success_rate_threshold:
                self.advance_level()