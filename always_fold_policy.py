# Random policy agent for poker
class Always_Fold_Agent:
    def __init__(self):
        pass

    def __str__(self):
        return f"Always Fold Agent"

    #Return the action taken from the state of the game
    def take_action(self, state, opp_state):
        """
        return a random action (0 or 1) for this agent

        state: (player_hand, community_cards, history)
        """
        return 0