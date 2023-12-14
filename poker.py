from deck import Deck, Card

# Keep track of our game according to our rules
class PokerGame:
    # Initialize the deck to be standard 52-card deck
    def __init__(self):
        self._deck = Deck()
        self._actions = [0, 1] #0 is fold or pass, 1 is check or bet
        self._num_community_cards = 3
        self._num_player_cards = 2
        self._hands = [[], []] #hands[0] is player 1's hand, hands[1] is player 2's hand. Each hand is a list of Card objects
        self._community_cards = [] # List of Card objects that are the community cards
        self._history = [] #List of actions each player takes (0 or 1), always starts from P0's action.

    # Reset the game so we can start again
    def reset_game(self):
        self._deck.reset()
        self._hands = [[], []]
        self._community_cards = []
        self._history = []

    #Shuffle the deck of cards
    def shuffle_deck(self):
        self._deck.shuffle()
    
    # Deal the players cards and the community cards, from a shuffled deck of cards
    def deal_cards(self):
        # Deal P0 and P1 cards:
        for i in range(2):
            self._hands[i] = self._deck.deal(self._num_player_cards)

        # Deal community cards:
        self._community_cards = self._deck.deal(self._num_community_cards)

    #Determine whether the betting rounds have ended or not
    def betting_ended(self):
        return (self._history in [[0, 0], [0, 1, 0], [0, 1, 1], [1, 0], [1, 1]])
    
    def get_state(self, player):
        """ Return the state of the game for the given player. Returns a tuple: (player hand, community cards, betting history)

            player: which player to return the state for
        """
        return (self._hands[player], self._community_cards, self._history)

    def play(self, p0_policy, p1_policy):
        """ Play 1 game of simplified poker, return the result of the game

            p0_policy -- player 0's policy: has a function take_action() that takes in a state and returns action
            p1_policy -- player 1's policy
        """
        # First reset the game states
        self.reset_game()

        # Shuffle the deck of cards
        self.shuffle_deck()

        # Deal the player cards and the community cards
        self.deal_cards()

        # Print out results
        print(f"P1 Hand: {self._hands[0]}")
        print(f"P2 Hand: {self._hands[1]}")
        print(f"Community Cards: {self._community_cards}")
        print(f"Remaining in Deck: {self._deck.size()}")

        policies = [p0_policy, p1_policy]
        p = 0 #Always start from player 1

        while not self.betting_ended():
            action = policies[p].take_action(self.get_state(p))
            print(f"Player {p} choses: {action}")
            self._history.append(action)
            p = int(not p) # Next player

        print(f"Betting ended. History: {self._history}\n")