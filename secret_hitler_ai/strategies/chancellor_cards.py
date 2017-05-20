"""
Strategies for the chancellor to choose which policy to enact.
"""
import random

from secret_hitler_ai.deck import Card
from secret_hitler_ai.logging import Log
from secret_hitler_ai.player import Player, Name
from secret_hitler_ai.strategies.strategy_helpers import multi_3, multi_2, \
    baysian_markov_analysis
from typing import Tuple


def chancellor_choose_liberal_cards_analyze(player: Player, president: Name,
                                            cards: Card, deck: Tuple[int])->Card:
    """
    The chancellor chooses a liberal policy to enact if possible and also analyzes 
    the cards passed to them.
    
    :param player: The player making the choice.
    :param president: The president who passed the cards.
    :param cards: The cards that were passed.
    :param deck: The remaining policies of each type
    :return: The policy enacted.
    """
    l_remaining = deck[0]
    f_remaining = deck[1]
    tot_remaining = l_remaining + f_remaining

    prob_fff = multi_3(f_remaining) / multi_3(tot_remaining)
    prob_ffl = 3 * l_remaining * multi_2(f_remaining) / multi_3(tot_remaining)
    prob_fll = 3 * f_remaining * multi_2(l_remaining) / multi_3(tot_remaining)
    prob_lll = multi_3(l_remaining) / multi_3(tot_remaining)
    default_fp = player.initial_probs.fascist
    default_lp = 1 - default_fp
    old_fp = player.probabilities[president].fascist
    if Card.LIBERAL in cards:
        card = Card.LIBERAL
        if Card.LIBERAL in cards:
            new_prob = 1 - (prob_lll+prob_fll)*default_lp/(prob_lll+prob_fll*default_lp)
            message = 'Chancellor {} is adjusting prob for player {} due ' \
                      'to receiving 2 Liberal Cards'
        else:
            new_prob = (prob_fll*default_fp)/(prob_ffl*default_lp+prob_fll*default_fp)
            message = 'Chancellor {} is adjusting prob for player {} due to ' \
                      'receiving 1 Liberal Card and 1 Fascist Card'
    else:
        new_prob = 1 - (prob_fff+prob_ffl)*default_fp/(prob_fff+prob_ffl*default_fp)
        message = 'Chancellor {} is adjusting prob for player ' \
                  '{} due to receiving 2 Fascist Cards'
        card = Card.FASCIST
        # player.print_probs()

    new_prob = baysian_markov_analysis(new_prob, old_fp, default_fp)
    player.set_prob(president, new_prob)
    Log.log_probs(message.format(player.name, president))
    return card


def chancellor_choose_fascist_cards(player: Player, president: Name,
                                    cards: Card, deck: Tuple[int])->Card:
    """
    The chancellor chooses a fascist policy to enact if possible.

    :param player: The player making the choice.
    :param president: The president who passed the cards.
    :param cards: The cards that were passed.
    :param deck: The remaining policies of each type
    :return: The policy enacted.
    """
    if Card.FASCIST in cards:
        return Card.FASCIST
    else:
        return Card.LIBERAL


def random_chancellor_cards(player: Player, president: Name,
                            cards: Card, deck: Tuple[int])->Card:
    """
    The chancellor chooses a random policy to enact if possible.

    :param player: The player making the choice.
    :param president: The president who passed the cards.
    :param cards: The cards that were passed.
    :param deck: The remaining policies of each type
    :return: The policy enacted.
    """
    random.shuffle(cards)
    return cards[0]
