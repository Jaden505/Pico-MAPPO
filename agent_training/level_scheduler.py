# A schedular to gradually increase levels and their difficulty while 20% repeating recent episodes and 10% older episode to prevent forgetting

from collections import deque
import numpy as np

class LevelScheduler:
    def __init__(self, levels, start_idx=0):
        self.levels = levels
        self.current_level = levels[start_idx]
        self.level_idx = start_idx
        
        self.N_RECENT_LEVELS = 2 # Number of recent levels to sample from
        self.SUCCESS_RATE_WINDOW = 12 # Number of episodes to consider for success rate
        self.SUCCESS_RATE_THRESHOLD = 0.8 # Success rate threshold to level up
        self.SAMPLE_PROBABILITIES = [0.7, 0.2, 0.1] # Probabilities for current, recent, older levels
        self.recent_results = deque(maxlen=self.SUCCESS_RATE_WINDOW) # Store recent episode results (1 for success, 0 for fail)
        
    def sample_level(self):
        """Sample level based on self.current_level and recent levels with defined probabilities.
            Returns: sampled level
        """
        cp, rp, op = self.SAMPLE_PROBABILITIES
        probs = np.zeros(len(self.levels))
        probs[self.level_idx] = (cp if self.level_idx > 0 else 1.0) # 70% chance to sample current level (100% if first level)

        for i in range(self.level_idx, 0, -1):
            if self.level_idx - i < self.N_RECENT_LEVELS:
                if self.level_idx <= self.N_RECENT_LEVELS:
                    probs[i] += (rp + op) / self.N_RECENT_LEVELS  # Distribute 30% chance among recent levels if no older levels 
                else:
                    probs[i] += op / self.N_RECENT_LEVELS # 20% chance to sample recent levels
            else:
                probs[i] += op / (self.level_idx - self.N_RECENT_LEVELS) # 10% chance to sample older levels
                
        return np.random.choice(self.levels, p=probs)
    
    def advance_level(self):
        """Advance to the next level
            Returns: bool: True if level advanced, False if already at highest level
        """
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
        """Record the result of an episode
            Args:
                level_idx: int: index of the level played
                success: bool: whether the episode was successful
        """
        if level_idx == self.level_idx:
            self.recent_results.append(1 if success else 0) # Record only if the level matches current level
        
        if success:
            succes_rate = sum(self.recent_results) / len(self.recent_results)
            if len(self.recent_results) == self.SUCCESS_RATE_WINDOW and succes_rate >= self.SUCCESS_RATE_THRESHOLD:
                self.advance_level()
    
    @property
    def n_levels(self):
        return len(self.levels)