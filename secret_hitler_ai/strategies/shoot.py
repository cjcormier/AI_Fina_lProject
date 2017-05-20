"""
Strategies to decide who to shoot.
"""
import random
from secret_hitler_ai.player import Player, Name
from typing import List


def liberal_shoot(player: Player, valid_players: List[Name]):
    """
    Shoot the player who is the most likely to be fascist.
    
    :param player: The player who is choosing whom to shoot.
    :param valid_players: The players who are able of being the chancellor.
    :return: The player to shoot
    """
    return player.max_fascist(valid_players)


def fascist_shoot(player: Player, valid_players: List[Name]):
    """
    Shoot the a liberal player.
    
    :param player: The player who is choosing whom to shoot.
    :param valid_players: The players who are able of being the chancellor.
    :return: The player to shoot
    """
    liberal_players = [x for x in valid_players if x not in player.fascists
                       and x is not player.hitler]
    return random.choice(liberal_players)


def hitler_shoot(player: Player, valid_players: List[Name]):
    """
    Shoot the player who is the least likely to be fascist.
    
    :param player: The player who is choosing whom to shoot.
    :param valid_players: The players who are able of being the chancellor.
    :return: The player to shoot
    """
    return player.min_fascist(valid_players)


def shoot_random(player: Player, valid_players: List[Name]):
    """
    Shoot a random player.
    
    :param player: The player who is choosing whom to shoot.
    :param valid_players: The players who are able of being the chancellor.
    :return: The player to shoot
    """
    return random.choice(valid_players)
