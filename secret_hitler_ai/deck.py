"""
Contains the basic classes to control and retrieve information about the Policy deck.
"""
from enum import unique, Enum
from random import randint
from typing import List, Tuple


@unique
class Card(Enum):
    """The types of policy cards."""
    FASCIST = 0
    LIBERAL = 1


class Deck:
    """The policy deck.
    
    The deck does not remember the order of the cards in the deck. The next card is 
    determined when it is drawn.
    """
    def __init__(self, liberal: int, fascist: int):
        self.libDeck = liberal
        self.facDeck = fascist
        self.facDisc = 0
        self.libDisc = 0

    def draw(self)->Card:
        """Draws a card.
        
        :return: The Drawn card.
        """
        if self.libDeck + self.facDeck <= 2:
            self.libDeck += self.libDisc
            self.facDeck += self.facDisc
            self.libDisc = 0
            self.facDisc = 0

        card = randint(0, self.libDeck + self.facDeck - 1)
        if card < self.libDeck:
            self.libDeck -= 1
            card = Card.LIBERAL
        else:
            self.facDeck -= 1
            card = Card.FASCIST
        return card

    def draw_hand(self)->List[Card]:
        """Draws three cards.
        
        :return: The drawn cards.
        """
        c1 = self.draw()
        c2 = self.draw()
        c3 = self.draw()
        return [c1, c2, c3]

    def discard(self, discard: List[Card], ignore: List[Card]):
        """Discards the unused cards.
        
        :param discard: The cards to discard.
        :param ignore: The cards to ignore and not discard.
        """
        for card in ignore:
            discard.remove(card)
        for card in discard:
            if card is Card.LIBERAL:
                self.libDisc += 1
            else:
                self.facDisc += 1

    def total_remaining(self)->Tuple[int, int]:
        """Returns the total remaining cards in play.
        
        :return: The counts of the remaining cards of each type.
        """
        return self.libDeck+self.libDisc, self.facDeck+self.facDisc


__all__ = ['Deck', 'Card']
