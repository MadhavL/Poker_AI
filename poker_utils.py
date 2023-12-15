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

def straight_flush_exists(hand, community):
    """
    Given a hand (list of Cards) and the community cards (list of Cards), determine whether a straight flush exists. 
    If yes, return the (sorted in descending order) ranks of the best flush (top card, then second top card), if no, return None
    """
    # Find best straight flush for 1 player card + 1 community card
    player_card_rank = hand[0].rank()
    player_card_suit = hand[0].suit()
    max_straight_flush = 0
    for card in community:
        if card.rank() == player_card_rank + 1 and card.suit() == player_card_suit:
            if card.rank() > max_straight_flush:
                max_straight_flush = card.rank()
        elif card.rank() == player_card_rank - 1 and card.suit() == player_card_suit:
            if player_card_rank > max_straight_flush:
                max_straight_flush = player_card_rank
    return max_straight_flush

def determine_best_hand(hand, community):
    """
    Given a hand (list of Cards) and the community cards (list of Cards), 
    determine the best hand using 1 card from the hand + 1 card from community cards
    
    Return the type of hand and the value of the hand.
    Type: 0 = High card, 1 = flush, 2 = straight, 3 = pair, 4 = straight flush
    Value: the value used to compare 2 hands of the same kind
    """
    straight_flush = straight_flush_exists(hand, community)
    if straight_flush != 0:
        return 4, straight_flush
    
    pair = pair_exists(hand, community)
    if pair != 0:
        return 3, pair
    
    straight = straight_exists(hand, community)
    if straight != 0:
        return 2, straight
    
    flush = flush_exists(hand, community)
    if flush != 0:
        return 1, flush
    
    else:
        return 0, hand[0].rank()