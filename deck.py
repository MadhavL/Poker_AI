import itertools as it
import random

class Card:
    def __init__(self, rank, suit):
        """ Creates a card of the given rank and suit.

            rank -- an integer
            suit -- a character
        """
        self._rank = rank
        self._suit = suit
        self._hash = str(self).__hash__() #Create a hash value from the string representation of the object
            

    def rank(self):
        return self._rank


    def suit(self):
        return self._suit

    #Check if 2 cards have same suit
    def same_suit(self, other):
        return self._suit == other._suit


    def __repr__(self):
        return "" + str(self._rank) + str(self._suit)

    #Check if 2 cards are the same with ==
    def __eq__(self, other):
        return self._rank == other._rank and self._suit == other._suit


    def __hash__(self):
        return self._hash

# Standard 52 card deck
class Deck:
    #Creates a list of Card objects (for each card in a deck)
    def __init__(self):
        """ Creates a standard deck of 52 cards including the given number of copies
            of each possible combination of the given ranks and the
            given suits.
        """
        self._cards = []
        self._ranks = range(1, 14) #Ace to King
        self._suits = ['S', 'H', 'D', 'C'] #Spades, Hearts, Diamonds, Clubs
        self._cards.extend(map(lambda c: Card(*c), it.product(self._ranks, self._suits))) #Create a cartesian product of rank & suit (becomes a tuple), pass each one of those into the map that unpacks the tuple and creates a card out of it

    #Shuffle the list of cards      
    def shuffle(self):
        """ Shuffles this deck. """
        random.shuffle(self._cards)

    def size(self):
        """ Returns the number of cards remaining in this deck. """
        return len(self._cards)
    

    def deal(self, n):
        """ Removes and returns the next n cards from this deck.

            n -- an integer between 0 and the size of this deck (inclusive)
        """
        dealt = self._cards[-n:] #The "Top" of the deck is the end of the list
        dealt.reverse() #Order it so that top card is first, top-nth card is last
        del self._cards[-n:] #Remove those cards from the deck
        return dealt

    # Hidden function: don't want the client to be able to access this (only for debugging purposes)
    def _peek(self, n):
        """ Returns the next n cards from this deck without removing them.

            n -- an integer between 0 and the size of this deck (inclusive)
        """
        dealt = self._cards[-n:]
        dealt.reverse()
        return dealt

            
    def remove(self, cards):
        """ Removes the given cards from this deck.  If there is a card
            to remove that isn't present in this deck, then the effect is
            the same as if that card had not been included in the list to
            remove.  If there are multiple occurrences of a given card
            in the list to remove, then the corresponding number of occurrences
            of that card in this deck are removed.

            cards -- an iterable over Cards
        """
        #Keep track of how many time each card occurs in the cards to remove list
        counts = dict()
        for card in cards:
            if card not in counts:
                counts[card] = 0
            counts[card] += 1

        #Remove the cards from the deck and return the modified deck
        remaining = []
        for card in self._cards:
            if card in counts and counts[card] > 0:
                counts[card] -= 1
            else:
                remaining.append(card)
        self._cards = remaining

    # Reset the deck back to original state
    def reset(self):
        self._cards = []
        self._cards.extend(map(lambda c: Card(*c), it.product(self._ranks, self._suits))) #Create a cartesian product of rank & suit (becomes a tuple), pass each one of those into the map that unpacks the tuple and creates a card out of it
