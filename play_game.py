from poker import PokerGame
from random_policy import Random_Agent
if __name__ == "__main__":
    num_games = 2
    game = PokerGame()
    random_agent = Random_Agent()
    for i in range(num_games):
        game.play(random_agent, random_agent)