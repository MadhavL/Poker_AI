import torch.nn as nn
import random
from collections import namedtuple, deque
import numpy as np

class DQNNetwork(nn.Module):
    def __init__(self, state_size=213, action_size=2):
        super(DQNNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 1024)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(1024, 128)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(128, action_size)

    def forward(self, x):
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        return self.fc3(x)

Experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])

class ReplayBuffer(object):
    def __init__(self, buffer_size, batch_size):
        self.memory = deque([], maxlen=buffer_size)
        self.batch_size = batch_size

    def add(self, *args):
        e = Experience(*args)
        self.memory.append(e)

    def sample(self):
        return random.sample(self.memory, k=self.batch_size)

    def __len__(self):
        return len(self.memory)

def card_to_index(card):
    """ Convert a card to a unique index between 0 and 51. """
    suit_order = {'C': 0, 'D': 13, 'H': 26, 'S': 39}  # Assuming suits are 'C', 'D', 'H', 'S'
    return suit_order[card.suit()] + card.rank() - 1  # Assuming rank starts at 1

def encode_card(card):
    """ Convert a card object to a one-hot encoded vector. """
    index = card_to_index(card)
    encoded = np.zeros(52)
    encoded[index] = 1
    return encoded

def encode_hand(hand):
    """ Encode a hand of cards (list of Card objects) into a one-hot encoded vector. """
    encoded_hand = [encode_card(card) for card in hand]
    return np.concatenate(encoded_hand)