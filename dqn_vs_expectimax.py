from poker import PokerGame
from random_policy import Random_Agent
from expectimax import ExpectimaxAgent
from always_bet_policy import Always_Bet_Agent
from always_fold_policy import Always_Fold_Agent
import numpy as np
from dqn_agent import DQNAgent

# Simulate the game with your policy agent
if __name__ == "__main__":
    num_training_games = 10000
    num_games = 25000 #How many games to simulate
    game = PokerGame() #Initialize the game model

    # Agent must have a take_action() function from: state (hand, community card, betting history) -> action in range [0, 1]

    #Initialize your agents
    p0_agent = DQNAgent()
    p1_agent = Random_Agent()
    #P0 is the first agent, P1 is the second agent. We will exchange which agent bets first in the simulations

    p0_wins = 0
    p0_reward = 0
    ties = 0
    
    
    """for i in range(num_training_games):
        game.reset_game()
        game.shuffle_deck()
        game.deal_cards()
        done = False
        while not done:
            # Get the state for player 0
            raw_state_p0 = game.get_state(0)  # This is a tuple

            # Transform this state into the DQN agent's expected format
            transformed_state_p0 = p0_agent.get_state(raw_state_p0)

            # DQN agent takes an action based on the transformed state
            action_p0 = p0_agent.take_action(raw_state_p0)

            # Apply the action to the game and get the result
            next_raw_state_p0, reward_p0, done = game.apply_action(0, action_p0)

            # Transform the next state into the DQN agent's expected format
            next_transformed_state_p0 = p0_agent.get_state(next_raw_state_p0)

            # Update the DQN agent
            p0_agent.step(transformed_state_p0, action_p0, reward_p0, next_transformed_state_p0, done)"""


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
        else:
            winner, margin = game.play(p1_agent, p0_agent, verbose=False)
            if winner == -1:
                p0_wins += 1 #Since p0 was put as p1 in the simulation
            elif winner == 0:
                ties += 1
            p0_reward -= margin
    print(f"{p0_agent} vs {p1_agent}\n{num_games} games.\nP0 avg reward/game: {(p0_reward/num_games):.2f}\nP0 win: {(p0_wins/num_games) * 100:.2f}%. Tie: {(ties/num_games) * 100:.2f}%. P1 win: {((num_games-ties-p0_wins)/num_games) * 100:.2f}%")