"""
Strategies for a president to choose a chancellor from a list of valid players.
"""
import random

from secret_hitler_ai.player import Player, Name
from typing import List


def choose_liberal_chancellor(player: Player, valid_players: List[Player]):
    """
    The player chooses the valid player who they think is most likely to be liberal.
    
    Ties are broken randomly.
    
    :param player: The player who is choosing the chancellor
    :param valid_players: The players who are able of being the chancellor.
    :return: The player chosen to be chancellor.
    """
    min_prob = 1
    players = []
    probabilities = player.probs
    for curr_player in valid_players:
        prob = probabilities[curr_player].fascist
        if prob < min_prob:
            min_prob = prob
            players = [curr_player]
        elif prob == min_prob:
            players.append(curr_player)
    choices = players if len(players) > 0 else valid_players
    return random.choice(choices)


def choose_fascist_chancellor(player: Player, valid_players: List[Name]):
    """
    The player chooses the valid player who they think is actually fascist.
    
    :param player: The player who is choosing the chancellor
    :param valid_players: The players who are able of being the chancellor.
    :return: The player chosen to be chancellor.
    """
    probabilities = player.probs
    fascist_players = []
    for valid_player in valid_players:
        if probabilities[valid_player].fascist == 1:
            fascist_players.append(valid_player)
    if len(fascist_players) == 0:
        return choose_liberal_chancellor(player, valid_players)
    return random.choice(fascist_players)


def choose_most_fascist_chancellor(player: Player, valid_players: List[Name]):
    """
    The player chooses the valid player who they think is most likely to be fascist.
    
    Ties are broken randomly.
    
    :param player: The player who is choosing the chancellor
    :param valid_players: The players who are able of being the chancellor.
    :return: The player chosen to be chancellor.
    """
    max_prob = 0
    players = []
    probabilities = player.probs
    for valid_player in valid_players:
        prob = probabilities[valid_player].fascist
        if prob > max_prob:
            max_prob = prob
            players = [valid_player]
        elif prob == max_prob:
            players.append(valid_player)
    players = players if len(players) > 0 else valid_players
    return random.choice(players)


def choose_not_hitler_chancellor(player: Player, valid_players: List[Name]):
    """
    The player chooses the valid player who they think is not Hitler.
    
    Ties are broken randomly.
    
    :param player: The player who is choosing the chancellor
    :param valid_players: The players who are able of being the chancellor.
    :return: The player chosen to be chancellor.
    """
    probabilities = player.probs
    fascist_players = []

    for curr_player in valid_players:
        if curr_player in probabilities:
            if probabilities[curr_player][1] != 1:
                fascist_players.append(curr_player)
    choices = fascist_players if len(fascist_players) > 0 else valid_players
    return random.choice(choices)


def random_choose_chancellor(player: Player, valid_players: List[Player]):
    """
    The player chooses randomly.
    
    :param player: The player who is choosing the chancellor
    :param valid_players: The players who are able of being the chancellor.
    :return: The player chosen to be chancellor.
    """
    return random.choice(valid_players)