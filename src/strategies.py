import random
from enum import Enum, unique
from math import pow

from src.cards import Cards
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
    SHOOT = 8


def choose_liberal_chancellor(player, valid_players):
    min_prob = 1
    players = []
    probabilities = player.probabilities
    name = player.name
    for curr_player in valid_players:
        if curr_player != name:
            prob = probabilities[curr_player][0]
            if prob < min_prob:
                min_prob = prob
                players = [curr_player]
            elif prob == min_prob:
                players.append(curr_player)
    return random.choice(players)


def choose_fascist_chancellor(player, valid_players):
    probabilities = player.probabilities
    name = player.name
    fascist_players = []
    for valid_player in valid_players:
        if valid_player != name:
            if probabilities[valid_player][0] == 1:
                fascist_players.append(valid_player)
    if len(fascist_players) == 0:
        return choose_liberal_chancellor(player, valid_players)
    return random.choice(fascist_players)


def f_choose_liberal_chancellor(player, valid_players):
    probabilities = player.probabilities
    name = player.name
    liberal_players = []
    for valid_player in valid_players:
        if valid_player != name:
            if probabilities[valid_player][0] != 1:
                liberal_players.append(valid_player)
    if len(liberal_players) == 0:
        return choose_liberal_chancellor(player, valid_players)
    return random.choice(liberal_players)


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
            cards = [Cards.LIBERAL, Cards.FASCIST]
            random.shuffle(cards)
            return cards
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


def standard_liberal_vote(player, president, chancellor):
    probabilities = player.probabilities
    president_prob = probabilities[president][0]
    chancellor_prob = probabilities[chancellor][0]

    unknown_fascists = player.num_fascists - len(player.fascists)
    unknown_players = len(set(probabilities.keys())-set(player.fascists)-{player.name})
    default_individual_prob = unknown_fascists/unknown_players
    limit_prob = 2*default_individual_prob-default_individual_prob**2

    # if president == player.name:
    #     president_prob = 0
    #     limit_prob = default_individual_prob
    #
    # if chancellor == player.name:
    #     chancellor_prob = 0
    #     limit_prob = default_individual_prob

    return president_prob+chancellor_prob-(president_prob*chancellor_prob) < round(limit_prob+.01, 2)


def standard_fascist_vote(player, president, chancellor):
    fascist_pres = president in player.fascists
    chancellor_pres = chancellor in player.fascists

    return fascist_pres or chancellor


def analyze_revealed_card(player, president, chancellor, card, deck):
    l_remaining = deck[0]
    f_remaining = deck[1]
    tot_remaining = l_remaining + f_remaining
    tot_remaining_3 = multi_3(tot_remaining)
    prob_fff = multi_3(f_remaining)/tot_remaining_3
    prob_ffl = 3*l_remaining*multi_2(f_remaining)/tot_remaining_3
    prob_fll = 3*f_remaining*multi_2(l_remaining)/tot_remaining_3
    prob_lll = multi_3(l_remaining)/tot_remaining_3
    prob_cf = player.probabilities[president][0]
    prob_pf = player.probabilities[chancellor][0]
    prob_cl = 1 - prob_cf
    prob_pl = 1 - prob_pf
    prob_president = 0
    prob_chancellor = 0
    prev_pres = 0
    prev_chanc = 0
    if card is Cards.LIBERAL:
        prev_pres = prob_pl
        prev_chanc = prob_cl
        if prob_lll == 0:
            if prob_pl == 0:
                prob_chancellor = 1
                prob_president = 0
            elif prob_cl == 0:
                prob_president = 1
                prob_chancellor = 0
            elif prob_cf == 0 and prob_pl == 0:
                prob_president = 0
                prob_chancellor = 0
        else:
            prob_l = prob_lll + prob_fll*(prob_cl+prob_pl-prob_cl*prob_pl) + prob_ffl*prob_cl*prob_pl
            prob_president = (prob_lll + prob_fll + prob_ffl*prob_cl)*prob_pl
            prob_president /= prob_l
            prob_president = 1-prob_president
            prob_chancellor = (prob_lll + prob_fll + prob_ffl*prob_pl)*prob_cl
            prob_chancellor /= prob_l
            prob_chancellor = 1-prob_chancellor
    else:
        prev_pres = prob_pl
        prev_chanc = prob_cl
        prob_f = prob_fff + prob_ffl*(prob_cf+prob_pf-prob_cf*prob_pf) + prob_fll*prob_cf*prob_pf
        prob_president = (prob_fff+ prob_ffl+ prob_fll*prob_cf)*prob_pf
        prob_president /= prob_f

        prob_chancellor = (prob_fff+ prob_ffl+ prob_fll*prob_pf)*prob_cf
        prob_chancellor /= prob_f

    player.set_prob(president, adjust(prob_president, prev_pres))
    player.set_prob(chancellor, adjust(prob_chancellor, prev_chanc))

    # message = "Player {} analyzed new fascist policy enacted by president {} and chancellor {}"
    # print(message.format(player.name, president, chancellor))
    # player.print_probs()

adjust_factor = 2


def set_adjust_factor(new_adjust):
    global adjust_factor
    adjust_factor = new_adjust


def default_prob(player):
    probabilities = player.probabilities
    unknown_fascists = player.num_fascists - len(player.fascists)
    unknown_players = len(set(probabilities.keys())-set(player.fascists)-{player.name})
    return unknown_fascists/unknown_players


def adjust(prob, old_prob):
    if prob > 1:
        prob = 1
    elif prob < 0:
        prob = 0
    global adjust_factor
    if old_prob*prob == 0 or prob == old_prob:
        return prob

    pos_prob_range = 1 - old_prob

    if prob > old_prob:
        return pow((prob - old_prob) / pos_prob_range, adjust_factor) * pos_prob_range + old_prob
    else:
        return pow((prob) / old_prob, adjust_factor) * old_prob


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


def liberal_shoot(player):
    return player.max_fascist()


def fascist_shoot(player):
    liberal_players = [x for x in player.probabilities.keys() if x not in player.fascists and x is not player.hitler]
    return random.choice(liberal_players)


def hitler_shoot(player):
    return player.min_fascist()


def pass_strat(*args):
    pass
