from deck import Deck, Card
import poker_utils

# Keep track of our game according to our rules
class PokerGame:
    # Initialize the deck to be standard 52-card deck
    def __init__(self):
        self._deck = Deck()
        self._actions = [0, 1] #0 is fold or pass, 1 is check or bet
        self._num_community_cards = 3
        self._num_player_cards = 1
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
    
    def determine_game_result(self, verbose):
        """ Determine the result of a game in terminal state. 
        Returns:
            the winner: 1 for p0, -1 for p1
            the amount of chips won: +ve for p0 win, -ve for p1 win
        """
        assert(self.betting_ended())

        # First check cases where hands don't need to be evaluated:
        #Player 0 checks, 1 bets, 0 folds. P1 wins 1
        if self._history == [0, 1, 0]:
            return -1, -1
        
        #Player 0 bets, 1 folds. P0 wins 1
        elif self._history == [1, 0]:
            return 1, 1
        
        #Otherwise, evaluate the better hand
        reward = 1 if self._history == [0, 0] else 2

        # Note, since a complete hand is only 2 cards in total, and since in Poker only the highest hand plays,
        # then if in any category, both players have the same (non-zero) pair, straight, etc. then it must be a tie 
        # (there is no "kicker")

        #Check straight flush
        
        p0_straight_flush = poker_utils.straight_flush_exists(self._hands[0], self._community_cards)
        p1_straight_flush = poker_utils.straight_flush_exists(self._hands[1], self._community_cards)
        if verbose:
            print(f"P0 straight flush: {p0_straight_flush}")
            print(f"P1 straight flush: {p1_straight_flush}")

        # If anyone has a higher straight flush, that person wins.
        if p0_straight_flush > p1_straight_flush:
            return 1, reward #For now, the chips is not being calculated
        elif p1_straight_flush > p0_straight_flush:
            return -1, -reward
        elif p0_straight_flush == p1_straight_flush != 0:
            return 0, 0 #Tie!
        
        #Check pair

        p0_pair = poker_utils.pair_exists(self._hands[0], self._community_cards)
        p1_pair = poker_utils.pair_exists(self._hands[1], self._community_cards)
        if verbose:
            print(f"P0 pair: {p0_pair}")
            print(f"P1 pair: {p1_pair}")

        # If anyone has a higher pair, that person wins.
        if p0_pair > p1_pair:
            return 1, reward #For now, the chips is not being calculated
        elif p1_pair > p0_pair:
            return -1, -reward
        elif p0_pair == p1_pair != 0:
            return 0, 0 #Tie!
        
        #Check straight

        p0_straight = poker_utils.straight_exists(self._hands[0], self._community_cards)
        p1_straight = poker_utils.straight_exists(self._hands[1], self._community_cards)
        if verbose:
            print(f"P0 straight: {p0_straight}")
            print(f"P1 straight: {p1_straight}")

        # If anyone has a higher straight, that person wins.
        if p0_straight > p1_straight:
            return 1, reward #For now, the chips is not being calculated
        elif p1_straight > p0_straight:
            return -1, reward
        elif p0_straight == p1_straight != 0:
            return 0, 0 #Tie!
        
        #Check flush

        p0_flush = poker_utils.flush_exists(self._hands[0], self._community_cards)
        p1_flush = poker_utils.flush_exists(self._hands[1], self._community_cards)
        if verbose:
            print(f"P0 flush: {p0_flush}")
            print(f"P1 flush: {p1_flush}")
        if p0_flush and not p1_flush:
            return 1, reward #For now, the chips is not being calculated
        elif p1_flush and not p0_flush:
            return -1, -reward
        elif p0_flush and p1_flush:
            max_flush = max(p0_flush, p1_flush)
            if p0_flush == max_flush:
                if p1_flush == max_flush:
                    #Tie
                    return 0, 0
                else:
                    return 1, reward
            else:
                return -1, -reward
        
        #No pair, straight, or flush. Compare cards
        if verbose:
            print(f"P0 high card: {self._hands[0][0].rank()}")
            print(f"P1 high card: {self._hands[1][0].rank()}")
        if self._hands[0][0].rank() > self._hands[1][0].rank():
            return 1, reward
        elif self._hands[1][0].rank() > self._hands[0][0].rank():
            return -1, -reward
        
        # Tie
        return 0, 0


    def play(self, p0_policy, p1_policy, verbose=False):
        """ Play 1 game of simplified poker, return the result of the game and the margin of victory

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
        if verbose:
            print(f"P0 Hand: {self._hands[0]}")
            print(f"P1 Hand: {self._hands[1]}")
            print(f"Community Cards: {self._community_cards}\n")

        policies = [p0_policy, p1_policy]
        p = 0 #Always start from player 1

        while not self.betting_ended():
            action = policies[p].take_action(self.get_state(p))
            if verbose:
                print(f"Player {p} chooses: {action}")
            self._history.append(action)
            p = int(not p) # Next player

        if verbose:
            print(f"Betting ended. History: {self._history}\n")
        
        winner, margin = self.determine_game_result(verbose=verbose)
        if verbose:
            if winner == 1:
                print(f"P0 won {margin} chips\n\n")

            elif winner == -1:
                print(f"P1 won {-margin} chips\n\n")

            else:
                print("Tie\n")
        
        return winner, margin
