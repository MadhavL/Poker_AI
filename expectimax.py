import poker_utils
from deck import Deck

class ExpectimaxAgent():
    def __init__(self, bet_threshold=0.3, verbose=False):
        self._remaining_deck = Deck()
        #Define functions that check each of the hand types
        self._possible_hands = [lambda x, _: x[0].rank(), poker_utils.flush_exists, poker_utils.straight_exists, poker_utils.pair_exists, poker_utils.straight_flush_exists]
        self._verbose = verbose
        self._bet_threshold = bet_threshold

    def __str__(self):
        return f"Expectimax Agent (threshold = {self._bet_threshold})"
    
    #Return the action taken from the state of the game
    def take_action(self, state, opp_state):
        """
        return a random action (0 or 1) for this agent

        state: (player_hand, community_cards, history)
        """
        hand, community_cards, history = state
        hand_type, hand_value = poker_utils.determine_best_hand(hand, community_cards)
        if self._verbose:
            print(f"Best hand type: {hand_type}, Hand value: {hand_value}")

        # Get all possible cards in deck other than your card and community cards
        self._remaining_deck.reset()
        self._remaining_deck.remove(hand + community_cards)

        lose_count = 0
        for card in self._remaining_deck.peek(self._remaining_deck.size()):
            #First check which cards can beat you in the same hand type
            same_hand_value = self._possible_hands[hand_type]([card], community_cards)
            
            #If the card does have a hand with the same type
            if same_hand_value:
                #If the hand type is flush, can't use a normal compare since return isn't a number, but otherwise we can
                if hand_type == 1:
                    if same_hand_value == max(hand_value, same_hand_value):
                        lose_count += 1
                        if self._verbose:
                            print(f"{card} beats your hand in category {hand_type}")
                        continue
                else:
                    if same_hand_value > hand_value:
                        if self._verbose:
                            print(f"{card} beats your hand in category {hand_type}")
                        lose_count += 1
                        continue

            #If doesn't beat in own category, check if beats in other categories
            if hand_type + 1 < len(self._possible_hands):
                for i in range(hand_type + 1, len(self._possible_hands)):
                    if self._possible_hands[i]([card], community_cards):
                        if self._verbose:
                            print(f"{card} beats your hand in category {i}")
                        lose_count += 1
                        break
        
        if self._verbose:
            print(f"Your hand loses to {lose_count}/{self._remaining_deck.size()}")
        
        win_prob = 1 - lose_count / self._remaining_deck.size()
        if self._verbose:
            print(f"Expected win prob: {win_prob: .2f}")


        #Using heuristics for an expectimax agent. If our expected win probability is above our bet threshold, bet. Otherwise fold
        return int(win_prob > self._bet_threshold)