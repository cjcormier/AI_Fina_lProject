"""
Strategies to vote on a proposed government.
"""
from secret_hitler_ai.player import Player, Name


def standard_liberal_vote(player: Player, president: Name, chancellor: Name):
    """
    Votes to elect a government only if the probability that the proposed government is 
    less likely to have one fascist than random chance (kinda).
    
    :param player: The player voting on the proposed government.
    :param president: The proposed president.
    :param chancellor: The proposed chancellor.
    :return: The player's vote.
    """
    probabilities = player.probs
    president_prob = probabilities[president].fascist
    chancellor_prob = probabilities[chancellor].fascist

    unknown_fascists = player.num_fascists - len(player.fascists)
    unknown_players = len(probabilities) - len(player.fascists)
    unknown_players -= 1 if player not in player.fascists else 0
    if unknown_fascists == 0:
        default_individual_prob = 0
    else:
        default_individual_prob = unknown_fascists/unknown_players

    limit_prob = 2*default_individual_prob - default_individual_prob**2
    # adjust = .04 * (len(probabilities))**.66
    adjust = .07
    prob_fascist = president_prob + chancellor_prob - president_prob*chancellor_prob
    return prob_fascist < limit_prob + adjust


def standard_fascist_vote(player: Player, president: Name, chancellor: Name):
    """
    Votes to elect a government only if there is a fascist in the proposed government.
    
    :param player: The player voting on the proposed government.
    :param president: The proposed president.
    :param chancellor: The proposed chancellor.
    :return: The player's vote.
    """
    fascist_pres = president in player.fascists
    chancellor_pres = chancellor in player.fascists

    return fascist_pres or chancellor_pres


def vote_true(player: Player, president: Name, chancellor: Name):
    """
    Always votes true.

    :param player: The player voting on the proposed government.
    :param president: The proposed president.
    :param chancellor: The proposed chancellor.
    :return: The player's vote.
    """
    return True
