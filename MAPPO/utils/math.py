import torch

def softmax_log_probilities(logits):
    exp_logits = torch.exp(logits)
    logits = exp_logits / torch.sum(exp_logits, dim=-1, keepdim=True)
    return torch.log(logits + 1e-10)  # Adding a small constant to avoid log(0)