"""
Strategies to analyze the revealed card.
"""
from typing import Tuple

from secret_hitler_ai.deck import Card
from secret_hitler_ai.player import Player, Name
from secret_hitler_ai.strategies.strategy_helpers import multi_3, multi_2, \
    baysian_markov_analysis


def analyze_revealed_card(player: Player, president: Name, chancellor: Name,
                          card: Card, deck: Tuple[int]):
    """
    Analyze the revealed card.
    
    :param player: Player analyzing the enacted policy.
    :param president: The president who enacted the policy.
    :param chancellor: The chancellor who enacted the policy.
    :param card: The policy enacted.
    :param deck: The number of unenacted policies of eadch type.
    """
    l_remaining = deck[0]
    f_remaining = deck[1]
    tot_remaining = l_remaining + f_remaining
    tot_remaining_3 = multi_3(tot_remaining)
    prob_fff = multi_3(f_remaining)/tot_remaining_3
    prob_ffl = 3*l_remaining*multi_2(f_remaining)/tot_remaining_3
    prob_fll = 3*f_remaining*multi_2(l_remaining)/tot_remaining_3
    prob_lll = multi_3(l_remaining)/tot_remaining_3

    orig_prob_f = player.initial_probs.fascist
    orig_prob_l = 1 - orig_prob_f
    prev_pf = player.probabilities[president].fascist
    prev_cf = player.probabilities[chancellor].fascist

    if card is Card.LIBERAL:
        prob_l = prob_lll + prob_fll*(2*orig_prob_l-orig_prob_l**2) + \
                 prob_ffl*orig_prob_l**2
        prob_president = (prob_lll + prob_fll + prob_ffl*orig_prob_l)*orig_prob_l
        prob_president /= prob_l
        prob_president = 1-prob_president

        prob_chancellor = (prob_lll + prob_fll + prob_ffl*orig_prob_l)*orig_prob_l
        prob_chancellor /= prob_l
        prob_chancellor = 1-prob_chancellor
    else:
        prob_f = prob_fff + prob_ffl*(2*orig_prob_f-orig_prob_f**2) + \
                 prob_fll*orig_prob_f**2
        prob_president = (prob_fff+prob_ffl+prob_fll*orig_prob_f) * orig_prob_f
        prob_president /= prob_f
        prob_chancellor = (prob_fff+prob_ffl+prob_fll*orig_prob_f) * orig_prob_f
        prob_chancellor /= prob_f

    prob_president = baysian_markov_analysis(prob_president, prev_pf, orig_prob_f)
    prob_chancellor = baysian_markov_analysis(prob_chancellor, prev_cf, orig_prob_f)

    player.set_prob(president, prob_president)
    player.set_prob(chancellor, prob_chancellor)

    # message = "Player {} analyzed new fascist policy enacted by " \
    #           "president {} and chancellor {}"
    # Log.log_probs(message.format(player.name, president, chancellor))
    # player.print_probs()
