import poker_utils
from deck import Deck
import random
from poker import PokerGame
from expectimax import ExpectimaxAgent
from always_bet_policy import Always_Bet_Agent
from random_policy import Random_Agent



class CFR_Agent:

    def __init__(self, verbose=False):
        '''p0 refers to the CFR Agent; p1 refers to the opponent'''
        
        self._map_hand_type = {0: "HC", 1: "F", 2: "S", 3: "P", 4: "SF"}
        
        # CFR Agent stats
        self._p0_total_regret = {"SF": [0, 0], "P": [0, 0], "S": [0, 0], "F": [0, 0], "HC": [0, 0]} # initialized to 0 for [pass, bet] in all info sets
        self._p0_total_prob = {"SF": [0, 0], "P": [0, 0], "S": [0, 0], "F": [0, 0], "HC": [0, 0]} 

        self.train(num_games=25000) # train model for num_games games
    
    def __str__(self):
        return f"CFR minimization Agent"

    
    def get_info_set(self, state):
        '''Returns key (a str) that corresponds to the information set for a given state'''

        card, community_cards, history = state

        hand_type_idx, hand_value = poker_utils.determine_best_hand(card, community_cards)
    
        hand_type = self._map_hand_type[hand_type_idx]

        return hand_type

    
    def get_strategy(self, info_set):
        '''Samples positive regrets; Regrets are normalized'''

        # look at regrets for (pass, bet) in info_set + add the non-negative regrets to get positive_regret_sum
        total_regret = self._p0_total_regret[info_set]
        pass_total_regret = total_regret[0]
        bet_total_regret = total_regret[1]

        positive_regret_sum = max(0, pass_total_regret) + max(0, bet_total_regret) # use max(0, action_total_regret) to make sure I only include positive regrets

        curr_strategy = [0, 0]

        # get normalized probabilities
        if positive_regret_sum > 0:
            curr_strategy[0] = max(0, pass_total_regret) / positive_regret_sum
            curr_strategy[1] = max(0, bet_total_regret) / positive_regret_sum

        else:
            curr_strategy = [0.5, 0.5]

        return curr_strategy


    def get_average_strategy(self, info_set):

        total_prob = self._p0_total_prob[info_set]
        total = total_prob[0] + total_prob[1] 

        strategy = {}

        if total > 0:
            strategy[0] = total_prob[0] / total 
            strategy[1] = total_prob[1] / total 
        else:
            strategy = [0.5, 0.5]


        return strategy

    def train(self, num_games):
        '''Trains on an expectimax agent'''
        
        game = PokerGame()

        p0 = self

        ev_10 = ExpectimaxAgent(bet_threshold=0.1, verbose=False)
        ev_30 = ExpectimaxAgent(bet_threshold=0.3, verbose=False)
        ev_50 = ExpectimaxAgent(bet_threshold=0.5, verbose=False)
        ev_70 = ExpectimaxAgent(bet_threshold=0.7, verbose=False)
        ev_90 = ExpectimaxAgent(bet_threshold=0.9, verbose=False)
        always = Always_Bet_Agent()
        random = Random_Agent()
         
        
        p1_agents = [ev_10, ev_30, ev_50, ev_70, ev_90, always, random]
        n = len(p1_agents)

        for i in range(num_games):
            game.reset_game()
            game.shuffle_deck()
            game.deal_cards()

            p0_state = game.get_state(0)
            p1_state = game.get_state(1)

            
            p1 = p1_agents[i % n]
            
            if i % 2 == 0:
                winner, margin = game.play(p0, p1, verbose=False)
            
            else:
                winner, margin = game.play(p1, p0, verbose=False)

            


    def take_action(self, p0_state, p1_state):
        '''Called from poker.py
            Returns action'''


        info_set = self.get_info_set(p0_state)

        strategy = self.get_average_strategy(info_set)

        strategy = [0, 0] 
        
        if strategy[0] > strategy[1]:
            action = 0
            
        elif strategy[0] < strategy[1]:
            action = 1

        else:
            # decide randomly
            action = random.choice([0, 1])
        
        
        self.cfr(p0_state, p1_state)

        return action
        


    def update_stats(self, info_set, strategy, strat_val, action_values):
        

        for i in range(2):
            self._p0_total_regret[info_set][i] += (action_values[i] - strat_val)
            self._p0_total_prob[info_set][i] += strategy[i]


        
        
    def payoff(self, p0_state, p1_state, p0_action):

        p0_card, community_cards, p0_history = p0_state
        p1_card, community_cards, p1_history = p1_state

        # get p0_info_set + p1_info_set
        p0_info_set = self.get_info_set(p0_state)
        p1_info_set = self.get_info_set(p1_state)

        # if both players have the same info set, see which one is better
        # otherwise, the player with the better info set (hand type) wins

        info_sets = [p0_info_set, p1_info_set]

        winner = None

        if p0_info_set == p1_info_set:
            
            p0_type, p0_value = poker_utils.determine_best_hand(p0_card, community_cards)
            p1_type, p1_value = poker_utils.determine_best_hand(p1_card, community_cards)

            if p0_value > p1_value:
                winner = "p0"
            else:
                winner = "p1"

        
        else:
            if "SF" in info_sets:
                if p0_info_set == "SF":
                    winner = "p0"
                else:
                    winner = "p1"

            elif "P" in info_sets:
                if p0_info_set == "P":
                    winner = "p0"
                else:
                    winner = "p1"

            elif "S" in info_sets:
                if p0_info_set == "S":
                    winner = "p0"
                else:
                    winner = "p1"

            elif "F" in info_sets:
                if p0_info_set == "F":
                    winner = "p0"
                else:
                    winner = "p1"


        assert(winner != None)

        if p0_action == 0:
            if winner == "p0":
                return 1
            else:
                return -1

        else:
            if winner == "p0":
                return 3
            else:
                return -3



    def cfr(self, p0_state, p1_state):
        

        p0_card, community_cards, p0_history = p0_state
        p1_card, community_cards, p1_history = p1_state

        info_set = self.get_info_set(p0_state)
        strategy = self.get_strategy(info_set)

        strat_val = 0.0
        action_values = [0.0, 0.0]



        for i in range(2):
            action_values[i] = self.payoff(p0_state, p1_state, i)
            strat_val += (strategy[i] * action_values[i])

        
        # update stats
        self.update_stats(info_set, strategy, strat_val, action_values)


