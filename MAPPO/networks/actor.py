import torch.nn as nn

class Actor(nn.Module):
    def __init__(self, train):
        super.__init__()
        
        self.train = train
        
        state_shape = 100*1100 # Game state in feature vector
        teammates_info_shape = 3*10*(state_shape + 2) # Teammates state, action and reward from previous steps to understand intention
        
        self.flatten = nn.Flatten()
        self.model = nn.Sequential(
            nn.Linear(state_shape + teammates_info_shape, 3000),
            nn.ReLU(),
        )
        
        if self.train:
            self.model.train()
    
    def forward(self, x):
        x = self.flatten(x)
        logits = self.model(x)
        return logits
    
    