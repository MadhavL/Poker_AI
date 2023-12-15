import poker_utils

class ExpectimaxAgent():
    def __init__(self):
        pass

    #Return the action taken from the state of the game
    def take_action(self, state):
        """
        return a random action (0 or 1) for this agent

        state: (player_hand, community_cards, history)
        """
        hand, community_cards, history = state
        hand_type, hand_value = poker_utils.determine_best_hand(hand, community_cards)
        print(f"Best hand type: {hand_type}, Hand value: {hand_value}")
        return 0