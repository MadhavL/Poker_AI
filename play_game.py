# Simplified poker by: Max Velasco, Francisco Almeida, and Madhav Lavakare

from poker import PokerGame
from random_policy import Random_Agent
from expectimax import ExpectimaxAgent
from always_bet_policy import Always_Bet_Agent
from always_fold_policy import Always_Fold_Agent
from dqn_agent import DQNAgent
from cfr import CFR_Agent
import numpy as np


def play_matchup(p0_agent, p1_agent):

    p0_wins = 0
    p0_reward = 0
    ties = 0

    # p1_reward = 0

    #Simulate game
    for i in range(num_games):
        #NOTE: since there is an advantage to being P1, when evaluating 2 agents, we should alternate between which policy is P0 and P1 (equal number)
        # To simulate the agents swapping positions
        if i % 2 == 0:
            winner, margin = game.play(p0_agent, p1_agent, verbose=False) #Set Verbose to True if you want to see how the game plays out
            if winner == 1:
                p0_wins += 1 #Since p0 was put as p0 in the simulation
            elif winner == 0:
                ties += 1
            p0_reward += margin
            # p1_reward -= margin
        else:
            winner, margin = game.play(p1_agent, p0_agent, verbose=False)
            if winner == -1:
                p0_wins += 1 #Since p0 was put as p1 in the simulation
            elif winner == 0:
                ties += 1
            p0_reward -= margin
            # p1_reward += margin
    
    print(f"{p0_agent} vs {p1_agent}\n{num_games} games.\nP0 avg reward/game: {(p0_reward/num_games):.2f}\nP0 win: {(p0_wins/num_games) * 100:.2f}%. Tie: {(ties/num_games) * 100:.2f}%. P1 win: {((num_games-ties-p0_wins)/num_games) * 100:.2f}%\n")



# Simulate the game with your policy agent
if __name__ == "__main__":
    num_games = 25000 #How many games to simulate
    game = PokerGame() #Initialize the game model

    # Agent must have a take_action() function from: state (hand, community card, betting history) -> action in range [0, 1]
    always_bet_agent = Always_Bet_Agent()
    always_fold_agent = Always_Fold_Agent()
    random = Random_Agent()
    ev_30 = ExpectimaxAgent(bet_threshold=0.3, verbose=False)
    ev_50 = ExpectimaxAgent(bet_threshold=0.5, verbose=False)
    ev_70 = ExpectimaxAgent(bet_threshold=0.7, verbose=False)
    ev_80 = ExpectimaxAgent(bet_threshold=0.8, verbose=False)
    ev_90 = ExpectimaxAgent(bet_threshold=0.9, verbose=False)

    dqn = DQNAgent()
    cfr = CFR_Agent()
    
    agents = [always_bet_agent, always_fold_agent, random, dqn, cfr, ev_30, ev_50, ev_70, ev_80, ev_90]


    print("DQN vs. all agents")
    for p1 in agents:

        play_matchup(dqn, p1)


    print("\nCFR vs. all agents")    
    for p1 in agents:

        play_matchup(cfr, p1)