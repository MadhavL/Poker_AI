import torch
from dqn_utils import DQNNetwork, ReplayBuffer, encode_hand
import torch.optim as optim
import torch.nn as nn
import numpy as np  
import random
from deck import Card
from poker_utils import determine_best_hand

class DQNAgent:
    def __init__(self, state_size=213, action_size=2, epsilon=1, alpha=1e-4, gamma=0.99, tau=.005, buffer_size=10000, batch_size=64, verbose=False):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon 
        self.epsilon_start = epsilon
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.05
        self.alpha = alpha
        self.max_betting_history = 3
        self.tau = tau
        self.steps = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.verbose = verbose
        # Main network and target network
        self.network = DQNNetwork(state_size, action_size).to(self.device)
        self.target_network = DQNNetwork(state_size, action_size).to(self.device)
        self.target_network.load_state_dict(self.network.state_dict())
        self.target_network.eval()  # Target network will not be trained

        self.optimizer = optim.AdamW(self.network.parameters(), lr= self.alpha, amsgrad=True)
        self.memory = ReplayBuffer(buffer_size, batch_size)

    def step(self, state, action, reward, next_state, done):
        self.memory.add(state, action, reward, next_state, done)
        if len(self.memory) > self.memory.batch_size:
            experiences = self.memory.sample()
            self.learn(experiences)

    """def take_action(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
        self.network.eval()
        with torch.no_grad():
            action_values = self.network(state)
        self.network.train()

        if random.random() > self.epsilon:
            return np.argmax(action_values.cpu().data.numpy())
        else:
            return random.choice(np.arange(self.action_size))"""



    def get_state(self, state):
        player_hand, community_cards, betting_history = state
            # Determine the best hand
        best_hand_type, best_hand_value = determine_best_hand(player_hand, community_cards)
        
        if isinstance(best_hand_value, (list, tuple)):
            best_hand_value = max(best_hand_value)  # Example: choose the highest value

        
        player_hand_vector = encode_hand(player_hand)
        community_cards_vector = encode_hand(community_cards)

        # Include the type and value of the best hand in the state vector
        best_hand_vector = np.array([best_hand_type, best_hand_value])  # Convert to float if necessary

        # Betting history
        betting_history_vector = np.pad(betting_history, 
                                (0, self.max_betting_history - len(betting_history)), 
                                'constant', 
                                constant_values=-1)


        # Concatenate all parts to form the state vector
        state_vector = np.concatenate([player_hand_vector, community_cards_vector, best_hand_vector, betting_history_vector])
        if self.verbose:
            print(f"Hand: {player_hand}, {best_hand_value}\nCommunity: {community_cards}\nBetting History: {betting_history}")
        return state_vector
    
    def update_epsilon(self):
        self.epsilon = self.epsilon_min + (self.epsilon_start - self.epsilon_min) * np.exp(-1 * self.steps / self.epsilon_decay)

    
    def take_action(self, state_tuple):
        # Process the state tuple to get a flat, numeric vector
        state_vector = self.get_state(state_tuple)
        
        # Convert the state vector to a PyTorch tensor
        state_tensor = torch.from_numpy(state_vector.astype(np.float32)).unsqueeze(0).to(self.device)
        self.network.eval()
        self.update_epsilon()
        with torch.no_grad():
            action_values = self.network(state_tensor)
        self.network.train()
        self.steps += 1
        # Choose action based on the Q-values
        action = np.argmax(action_values.cpu().data.numpy()) if random.random() > self.epsilon else random.choice(np.arange(self.action_size))
        if self.verbose: print(f"Action: {action}")
        # self.update_epsilon()
        return action
        
    def learn(self, experiences):
        states, actions, rewards, next_states, dones = zip(*experiences)
        states = torch.from_numpy(np.vstack(states)).float().to(self.device)
        actions = torch.from_numpy(np.vstack(actions)).long().to(self.device)
        rewards = torch.from_numpy(np.vstack(rewards)).float().to(self.device)
        next_states = torch.from_numpy(np.vstack(next_states)).float().to(self.device)
        dones = torch.from_numpy(np.vstack(dones).astype(np.uint8)).float().to(self.device)

        Q_targets_next = self.target_network(next_states).detach().max(1)[0].unsqueeze(1)
        Q_targets = rewards + (self.gamma * Q_targets_next * (1 - dones))

        Q_expected = self.network(states).gather(1, actions)

        loss = nn.MSELoss()(Q_expected, Q_targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.epsilon = max(self.epsilon_min, self.epsilon_decay * self.epsilon)

        # Update target network
        self.soft_update(self.network, self.target_network)

    def soft_update(self, local_model, target_model):
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(self.tau*local_param.data + (1.0-self.tau)*target_param.data)


    def __str__(self):
        return "DQN Agent"
    