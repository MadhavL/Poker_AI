from poker import PokerGame

if __name__ == "__main__":
    num_games = 2
    game = PokerGame()
    for i in range(num_games):
        game.play()