"""
Strategies for the president to choose which policy to pass to the chancellor.
"""
import random

from secret_hitler_ai.deck import Card
from secret_hitler_ai.player import Player, Name
from typing import List


def president_choose_liberal_cards(player: Player, chancellor: Name,
                                   cards: List[Card])->List[Card]:
    """
    The player passes as many liberal policy as possible.
    
    :param player: The player making the decision.
    :param chancellor: The chancellor that the policies are being passed to.
    :param cards: The drawn cards.
    :return: Cards 
    """
    if Card.FASCIST in cards:
        cards.remove(Card.FASCIST)
    else:
        cards.pop()
    return cards


def president_give_choice(player: Player, chancellor: Name,
                          cards: List[Card])->List[Card]:
    """
    The player attempts to pass a liberal and fascist policy.
    
    :param player: The player making the decision.
    :param chancellor: The chancellor that the policies are being passed to.
    :param cards: The drawn cards.
    :return: Cards 
    """
    if Card.LIBERAL in cards and Card.FASCIST in cards:
        cards = [Card.LIBERAL, Card.FASCIST]
        return cards
    else:
        cards.pop()
        return cards


def president_choose_fascist_cards(player: Player, chancellor: Name,
                                   cards: List[Card])->List[Card]:
    """
    The player passes as many fascist cards as possible.
    
    :param player: The player making the decision.
    :param chancellor: The chancellor that the policies are being passed to.
    :param cards: The drawn cards.
    :return: Cards 
    """
    if Card.LIBERAL in cards:
        cards.remove(Card.LIBERAL)
    else:
        cards.pop()
    return cards


def random_president_cards(player: Player, chancellor: Name,
                                   cards: List[Card])->List[Card]:
    """
    The player passes two random cards.
    
    :param player: The player making the decision.
    :param chancellor: The chancellor that the policies are being passed to.
    :param cards: The drawn cards.
    :return: Cards 
    """
    cards.pop()
    return cards
