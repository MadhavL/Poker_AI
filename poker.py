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
        self._history = [] #List of actions each player takes (0 or 1), always starts from P1's action.

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
        # Deal P1 and P2 cards:
        for i in range(2):
            self._hands[i] = self._deck.deal(self._num_player_cards)

        # Deal community cards:
        self._community_cards = self._deck.deal(self._num_community_cards)

    # Play 1 game of simplified poker, return the result of the game
    def play(self):
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