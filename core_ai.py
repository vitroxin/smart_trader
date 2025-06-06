# core_ai.py
import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

class QuantumTrader(nn.Module):
    def __init__(self):
        super().__init__()
        self.quant = torch.quantization.QuantStub()
        self.lstm = nn.LSTM(input_size=10, hidden_size=64, num_layers=2, batch_first=True)
        self.attention = nn.MultiheadAttention(embed_dim=64, num_heads=4)
        self.fc = nn.Sequential(
            nn.Linear(64, 32),
            nn.SiLU(),
            nn.Linear(32, 3)  # Buy, Sell, Hold
        )
        self.dequant = torch.quantization.DeQuantStub()
        
    def forward(self, x):
        x = self.quant(x)
        x, _ = self.lstm(x)
        x = x.transpose(0, 1)
        x, _ = self.attention(x, x, x)
        x = x.mean(dim=0)
        x = self.fc(x)
        return self.dequant(x)

class MetaRLTrader:
    def __init__(self, device='cpu'):
        self.device = device
        self.policy_net = QuantumTrader().to(device)
        self.target_net = QuantumTrader().to(device)
        self.optimizer = optim.AdamW(self.policy_net.parameters(), lr=1e-4)
        self.memory = []
        self.batch_size = 32
        self.gamma = 0.99
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.policy_net.eval()
        self.target_net.eval()

    def predict(self, state):
        with torch.no_grad():
            state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            output = self.policy_net(state)
            return output.cpu().numpy()[0]

    def train(self):
        if len(self.memory) < self.batch_size:
            return
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states = zip(*batch)
        states = torch.FloatTensor(np.array(states)).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)

        current_q = self.policy_net(states).gather(1, actions.unsqueeze(1))
        next_q = self.target_net(next_states).max(1)[0].detach()
        expected_q = rewards + (self.gamma * next_q)

        loss = nn.MSELoss()(current_q.squeeze(), expected_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))
        if len(self.memory) > 10000:
            self.memory.pop(0)

    def save(self, path):
        torch.save(self.policy_net.state_dict(), path)

    def load(self, path):
        self.policy_net.load_state_dict(torch.load(path, map_location=self.device))
        self.target_net.load_state_dict(self.policy_net.state_dict())
