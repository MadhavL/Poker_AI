from collections import defaultdict
def pair_exists(hand, community):
    """
    Given a hand (list of Cards) and the community cards (list of Cards), determine whether a pair exists. 
    If yes, return the rank of the highest pair, if no, return 0
    """
    # Check for pair with hand card + 1 community card
    player_rank = hand[0].rank()
    for card in community:
        rank = card.rank()
        if rank == player_rank:
            return rank
    return 0

def straight_exists(hand, community):
    """
    Given a hand (list of Cards) and the community cards (list of Cards), determine whether a straight exists. 
    If yes, return the rank of the highest straight (top card), if no, return 0
    """
    # Find best straight for 1 player card + 1 community card
    player_rank = hand[0].rank()
    community_ranks = {card.rank() for card in community}
    if player_rank + 1 in community_ranks:
        return player_rank + 1
    elif player_rank - 1 in community_ranks:
        return player_rank
    else:
        return 0

def flush_exists(hand, community):
    """
    Given a hand (list of Cards) and the community cards (list of Cards), determine whether a flush exists. 
    If yes, return the (sorted in descending order) ranks of the best flush (top card, then second top card), if no, return None
    """
    # Combine hand + community cards into one list
    player_suit = hand[0].suit()
    flush = None
    max_flush = 0
    for card in community:
        if card.suit() == player_suit:
            if card.rank() > max_flush:
                flush = [hand[0].rank(), card.rank()]
                max_flush = card.rank()
    if not flush:
        return None
    return sorted(flush, reverse=True)