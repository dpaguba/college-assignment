import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import deque
from typing import List, Tuple, Optional

class DQNNetwork(nn.Module):
    """
    Deep Q-Network für Catan AI
    State Features + Action Features -> Q-Value
    """
    
    def __init__(self, state_size: int = 56, action_feature_size: int = 6, hidden_size: int = 256):
        super(DQNNetwork, self).__init__()
        
        self.state_size = state_size
        self.action_feature_size = action_feature_size
        
        # State Processing Network
        self.state_net = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(0.2),
        )
        
        # Action Processing Network  
        self.action_net = nn.Sequential(
            nn.Linear(action_feature_size, hidden_size // 4),
            nn.ReLU(),
            nn.Linear(hidden_size // 4, hidden_size // 4),
            nn.ReLU(),
        )
        
        # Combined Network (State + Action -> Q-Value)
        combined_size = (hidden_size // 2) + (hidden_size // 4)
        self.q_net = nn.Sequential(
            nn.Linear(combined_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size // 2, hidden_size // 4),
            nn.ReLU(),
            nn.Linear(hidden_size // 4, 1)  # Single Q-value output
        )
        
        # Initialize weights
        self.apply(self._init_weights)
    
    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.xavier_uniform_(module.weight)
            module.bias.data.fill_(0.01)
    
    def forward(self, state_features: torch.Tensor, action_features: torch.Tensor) -> torch.Tensor:
        """
        Forward pass: State + Action -> Q-Value
        
        Args:
            state_features: [batch_size, state_size]
            action_features: [batch_size, action_feature_size]
        
        Returns:
            Q-values: [batch_size, 1]
        """
        state_processed = self.state_net(state_features)
        action_processed = self.action_net(action_features)
        
        # Combine state and action features
        combined = torch.cat([state_processed, action_processed], dim=1)
        
        q_value = self.q_net(combined)
        return q_value

class ReplayBuffer:
    """
    Experience Replay Buffer für DQN Training
    """
    
    def __init__(self, capacity: int = 10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state_features: np.ndarray, action_features: np.ndarray, 
             reward: float, next_state_features: Optional[np.ndarray], 
             next_action_features_list: Optional[List[np.ndarray]], done: bool):
        """
        Fügt eine Erfahrung zum Buffer hinzu
        """
        experience = {
            'state_features': state_features,
            'action_features': action_features,
            'reward': reward,
            'next_state_features': next_state_features,
            'next_action_features_list': next_action_features_list,
            'done': done
        }
        self.buffer.append(experience)
    
    def sample(self, batch_size: int) -> List:
        """
        Sampelt eine Batch von Erfahrungen
        """
        return random.sample(self.buffer, batch_size)
    
    def __len__(self) -> int:
        return len(self.buffer)

class CatanDQNAgent:
    """
    DQN Agent für Catan
    """
    
    def __init__(self, state_size: int = 56, action_feature_size: int = 6, 
                 lr: float = 0.0001, gamma: float = 0.99, epsilon: float = 1.0,
                 epsilon_min: float = 0.01, epsilon_decay: float = 0.995,
                 memory_size: int = 10000, batch_size: int = 32):
        
        self.state_size = state_size
        self.action_feature_size = action_feature_size
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        
        # Neural Networks
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        self.q_network = DQNNetwork(state_size, action_feature_size).to(self.device)
        self.target_network = DQNNetwork(state_size, action_feature_size).to(self.device)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        
        # Copy weights to target network
        self.update_target_network()
        
        # Replay Buffer
        self.memory = ReplayBuffer(memory_size)
        
        # Training stats
        self.training_step = 0
        self.loss_history = []
    
    def update_target_network(self):
        """
        Kopiert Gewichte vom Haupt-Netzwerk zum Target-Netzwerk
        """
        self.target_network.load_state_dict(self.q_network.state_dict())
    
    def act(self, state_features: np.ndarray, action_features_list: List[np.ndarray], 
            training: bool = True) -> int:
        """
        Wählt eine Action basierend auf epsilon-greedy Policy
        
        Args:
            state_features: Aktuelle Spielzustand-Features
            action_features_list: Liste von Action-Features für alle möglichen Actions
            training: Ob gerade trainiert wird (für epsilon-greedy)
        
        Returns:
            Index der gewählten Action
        """
        if training and random.random() < self.epsilon:
            # Exploration: Random action
            return random.randint(0, len(action_features_list) - 1)
        
        # Exploitation: Beste Action basierend auf Q-Values
        return self._get_best_action(state_features, action_features_list)
    
    def _get_best_action(self, state_features: np.ndarray, 
                        action_features_list: List[np.ndarray]) -> int:
        """
        Wählt die Action mit dem höchsten Q-Value
        """
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state_features).unsqueeze(0).to(self.device)
            
            q_values = []
            for action_features in action_features_list:
                action_tensor = torch.FloatTensor(action_features).unsqueeze(0).to(self.device)
                q_value = self.q_network(state_tensor, action_tensor)
                q_values.append(q_value.item())
            
            return np.argmax(q_values)
    
    def remember(self, state_features: np.ndarray, action_features: np.ndarray,
                reward: float, next_state_features: Optional[np.ndarray],
                next_action_features_list: Optional[List[np.ndarray]], done: bool):
        """
        Speichert Erfahrung im Replay Buffer
        """
        self.memory.push(state_features, action_features, reward, 
                        next_state_features, next_action_features_list, done)
    
    def replay(self) -> Optional[float]:
        """
        Trainiert das Netzwerk mit einer Batch aus dem Replay Buffer
        
        Returns:
            Loss value oder None wenn nicht genug Erfahrungen vorhanden
        """
        if len(self.memory) < self.batch_size:
            return None
        
        batch = self.memory.sample(self.batch_size)
        
        # Prepare batch data
        state_features = torch.FloatTensor([e['state_features'] for e in batch]).to(self.device)
        action_features = torch.FloatTensor([e['action_features'] for e in batch]).to(self.device)
        rewards = torch.FloatTensor([e['reward'] for e in batch]).to(self.device)
        dones = torch.BoolTensor([e['done'] for e in batch]).to(self.device)
        
        # Current Q-values
        current_q_values = self.q_network(state_features, action_features).squeeze()
        
        # Calculate target Q-values
        target_q_values = rewards.clone()
        
        for i, experience in enumerate(batch):
            if not experience['done'] and experience['next_state_features'] is not None:
                next_state = torch.FloatTensor(experience['next_state_features']).unsqueeze(0).to(self.device)
                next_actions = experience['next_action_features_list']
                
                if next_actions:
                    # Get max Q-value for next state
                    with torch.no_grad():
                        next_q_values = []
                        for next_action_features in next_actions:
                            next_action_tensor = torch.FloatTensor(next_action_features).unsqueeze(0).to(self.device)
                            next_q = self.target_network(next_state, next_action_tensor)
                            next_q_values.append(next_q.item())
                        
                        max_next_q = max(next_q_values)
                        target_q_values[i] = rewards[i] + self.gamma * max_next_q
        
        # Compute loss
        loss = F.mse_loss(current_q_values, target_q_values)
        
        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        
        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), max_norm=1.0)
        
        self.optimizer.step()
        
        # Update epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        # Update target network periodically
        self.training_step += 1
        if self.training_step % 100 == 0:
            self.update_target_network()
        
        self.loss_history.append(loss.item())
        return loss.item()
    
    def save(self, filepath: str):
        """
        Speichert das trainierte Modell
        """
        torch.save({
            'q_network_state_dict': self.q_network.state_dict(),
            'target_network_state_dict': self.target_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'training_step': self.training_step,
            'loss_history': self.loss_history
        }, filepath)
        print(f"Model saved to {filepath}")
    
    def load(self, filepath: str):
        """
        Lädt ein trainiertes Modell
        """
        checkpoint = torch.load(filepath, map_location=self.device)
        
        self.q_network.load_state_dict(checkpoint['q_network_state_dict'])
        self.target_network.load_state_dict(checkpoint['target_network_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epsilon = checkpoint['epsilon']
        self.training_step = checkpoint['training_step']
        self.loss_history = checkpoint['loss_history']
        
        print(f"Model loaded from {filepath}")
        print(f"Training step: {self.training_step}, Epsilon: {self.epsilon:.4f}")