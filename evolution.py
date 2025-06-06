# evolution.py
import torch
import random

def mutate_model(model):
    with torch.no_grad():
        for param in model.parameters():
            if random.random() < 0.1:
                noise = torch.randn_like(param) * 0.01
                param.add_(noise)
    print("[evolution] Model mutated.")

def evolve(trader):
    # يمكن أن نضيف معايير تقييم وتحسين بناءً على الأداء
    mutate_model(trader.policy_net)
    trader.target_net.load_state_dict(trader.policy_net.state_dict())
