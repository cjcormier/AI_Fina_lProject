from enum import Enum, unique
from src.cards import *
import random

@unique
class Strategy_Types(Enum):
    CHOOSE_PRES = 1
    CHANCELLOR_CARDS = 2
    PRESIDENT_CARDS = 3
    VOTE = 4
    VOTE_RESULTS = 5
    ANALYZE_REVEALED_CARD = 6


def liberal_choose_chancellor(player, valid_players):
    min = 1.1
    players = []
    probabilities = player.probabilities
    if len(valid_players) < 0:
        print('No Valid Players')
        raise ValueError

    for player in valid_players:
        if player in probabilities:
            prob = probabilities[player][0]
            if prob < min:
                min = prob
                players = [player]
            elif prob == min:
                players.append(player)

    return random.choice(players)


def fascist_choose_fascist_chancellor(player, valid_players):
    probabilities = player.probabilities
    fascist_players = []
    for player in valid_players:
        if player in probabilities:
            if probabilities[player][0] == 1:
                fascist_players.append(player)
    return random.choice(fascist_players)


def fascist_choose_not_hitler_chancellor(player, valid_players):
    probabilities = player.probabilities
    fascist_players = []

    for player in valid_players:
        if player in probabilities:
            if probabilities[player][0] == 1:
                fascist_players.append(player)
    return random.choice(fascist_players)


def liberal_president_choose_cards(player, chancellor, cards):
    if Cards.FASCIST in cards:
        return cards.remove(Cards.FASCIST)
    else:
        return cards.pop()


def fascist_president_choose_cards(player, chancellor, cards):
    if Cards.LIBERAL in cards:
        return cards.remove(Cards.LIBERAL)
    else:
        return cards.pop()