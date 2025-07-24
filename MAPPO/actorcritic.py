import torch.nn as nn

class ActorCritic(nn.Module):
    def __init__(self, in_dim, out_dim):
        super.__init__()
        
        self.flatten = nn.Flatten()
        self.model = nn.Sequential(
            nn.Linear(in_dim, out_dim),
            nn.ReLU(),
        )
    
    def forward(self, x):
        x = self.flatten(x)
        logits = self.model(x)
        return logits
    
    