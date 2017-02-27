from enum import Enum, unique
from src.cards import Cards
import random
from src.roles import Role


@unique
class StrategyTypes(Enum):
    CHOOSE_CHANCELLOR = 1
    CHANCELLOR_CARDS = 2
    PRESIDENT_CARDS = 3
    VOTE = 4
    VOTE_RESULTS = 5
    ANALYZE_REVEALED_CARD = 6
    ANALYZE_CHANCELLOR_CARD = 7


def choose_liberal_chancellor(player, valid_players):
    min_prob = 1.1
    players = []
    probabilities = player.probabilities
    name = player.name

    for player in valid_players:
        if player is not name:
            prob = probabilities[player][0]
            if prob < min_prob:
                min_prob = prob
                players = [player]
            elif prob == min_prob:
                players.append(player)

    return random.choice(players)


def choose_fascist_chancellor(player, valid_players):
    probabilities = player.probabilities
    name = player.name
    fascist_players = []
    for valid_player in valid_players:
        if valid_player is not name:
            if probabilities[valid_player][0] == 1:
                fascist_players.append(valid_player)
    if len(fascist_players) == 0:
        return choose_liberal_chancellor(player, valid_players)
    return random.choice(fascist_players)


def choose_not_hitler_chancellor(player, valid_players):
    probabilities = player.probabilities
    fascist_players = []

    for player in valid_players:
        if player in probabilities:
            if probabilities[player][0] == 1:
                fascist_players.append(player)
    return random.choice(fascist_players)


def president_choose_liberal_cards(player, chancellor, cards):
    if Cards.FASCIST in cards:
        cards.remove(Cards.FASCIST)
    else:
        cards.pop()
    return cards


def president_give_choice(player, chancellor, cards):
    if Cards.LIBERAL in cards:
        if Cards.FASCIST in cards:
            return random.shuffle([Cards.LIBERAL, Cards.FASCIST])
    cards.pop()
    return cards


def president_choose_fascist_cards(player, chancellor, cards):
    if Cards.LIBERAL in cards:
        cards.remove(Cards.LIBERAL)
    else:
        cards.pop()
    return cards


def chancellor_choose_liberal_cards(player, president, cards, deck):
    if Cards.LIBERAL in cards:
        return Cards.LIBERAL
    else:
        l_remaining = deck[0]
        f_remaining = deck[1]
        tot_remaining = l_remaining + f_remaining

        prob_fff = multi_3(f_remaining)/multi_3(tot_remaining)
        prob_ffl = 3*l_remaining*multi_2(f_remaining)/multi_3(tot_remaining)

        old_prob = player.probabilities[president][0]

        new_prob = (prob_fff+prob_ffl)*old_prob/(prob_fff+prob_ffl*old_prob)

        player.set_prob(president, new_prob)
        message = 'Player {} is adjusting prob for player {} due to receiving 2 Fascist Cards'
        print(message.format(player.name, president))
        player.print_probs()
        return Cards.FASCIST


def multi_3(num):
    return num*(num-1)*(num-2)


def multi_2(num):
    return num*(num-1)


def chancellor_choose_fascist_cards(player, president, cards, deck):
    if Cards.FASCIST in cards:
        return Cards.FASCIST
    else:
        return Cards.LIBERAL


def standard_vote(player, president, chancellor):
    probabilities = player.probabilities
    president_prob = probabilities[president][0]
    chancellor_prob = probabilities[chancellor][0]

    if president is player.name and player.probabilities[player.name] == 1:
        president_prob = 0

    if chancellor is player.name and player.probabilities[player.name] == 1:
        chancellor_prob = 0

    return president_prob+chancellor_prob-(president_prob*chancellor_prob) < .7


def analyze_revealed_card(player, president, chancellor, deck):
    pass


def analyze_chancellor_card(player, chancellor, pres_cards, chanc_card):
    if chanc_card == Cards.FASCIST and Cards.LIBERAL in pres_cards:
        print("Player {} thinks chancellor {} is a Fascist.".format(player.name, chancellor))
        known_roles = {Role.FASCIST: player.fascists, Role.HITLER: player.hitler}
        if chancellor not in known_roles[Role.FASCIST]:
            known_roles[Role.FASCIST].append(chancellor)

        hitler_prob = 0
        if len(known_roles[Role.FASCIST]) == player.num_fascists:
            hitler_prob = 1 / (len(player.probabilities) - 1)

        player.known_roles = known_roles
        player.set_prob(chancellor, 1, hitler_prob)


def pass_strat(*args):
    pass
