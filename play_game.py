from poker import PokerGame
from random_policy import Random_Agent
import numpy as np

# Simulate the game with your policy agent
if __name__ == "__main__":
    num_games = 1000 #How many games to simulate
    game = PokerGame() #Initialize the game model
    random_agent = Random_Agent() #Initialize your agent. 
    # Agent must have a take_action() function from: state (hand, community card, betting history) -> action in range [0, 1]

    #Simulate the game
    player_wins = []
    game_margins = []
    for i in range(num_games):
        winner, margin = game.play(random_agent, random_agent, verbose=False) #Set Verbose to True if you want to see how the game plays out
        #NOTE: since there is an advantage to being P1, when evaluating 2 agents, we should alternate between which policy is P0 and P1 (equal number)
        # To simulate the agents swapping positions
        if i % 2 == 1:
            winner = -winner
            margin = -margin
        player_wins.append(winner)
        game_margins.append(margin)
    print(f"Average winner: {np.mean(player_wins)}. Average reward: {np.mean(game_margins)}")