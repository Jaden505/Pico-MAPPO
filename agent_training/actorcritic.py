import torch.nn as nn
import torch

class ActorCritic(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        
        print(f"Initializing ActorCritic with input dimension {in_dim} and output dimension {out_dim}")
        
        self.model = nn.Sequential(
            nn.Linear(in_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, out_dim)
        )
    
    def forward(self, x):
        logits = self.model(x)
        return logits
    