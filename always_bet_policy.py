# Random policy agent for poker
class Always_Bet_Agent:
    def __init__(self):
        pass

    #Return the action taken from the state of the game
    def take_action(self, state):
        """
        return a random action (0 or 1) for this agent

        state: (player_hand, community_cards, history)
        """
        return 1