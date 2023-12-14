def pair_exists(hand, community):
    """
    Given a hand (list of Cards) and the community cards (list of Cards), determine whether a pair exists. 
    If yes, return the rank of the highest pair, if no, return 0
    """
    # Combine hand + community cards into one list
    all_cards = hand + community
    cards = set()
    max_pair = 0
    for card in all_cards:
        rank = card.rank()
        if rank in cards:
            if rank > max_pair:
                max_pair = rank
        else:
            cards.add(rank)
    return max_pair

def straight_exists(hand, community):
    """
    Given a hand (list of Cards) and the community cards (list of Cards), determine whether a pair exists. 
    If yes, return the rank of the highest straight (top card), if no, return 0
    """
    # Combine hand + community cards into one list
    all_cards = hand + community
    cards = set()
    max_straight = 0
    for card in all_cards:
        rank = card.rank()
        if rank - 1 in cards:
            if rank > max_straight:
                max_straight = rank
        elif rank + 1 in cards:
            if rank + 1 > max_straight:
                max_straight = rank + 1
        else:
            cards.add(rank)
    return max_straight
