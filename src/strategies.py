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

    return president_prob+chancellor_prob-(president_prob*chancellor_prob) < round(limit_prob+.005, 2)

def standard_fascist_vote(player, president, chancellor):
    fascist_pres = president in player.fascists
    chancellor_pres = chancellor in player.fascists

    return fascist_pres or chancellor


def analyze_revealed_card(player, president, chancellor, card, deck):
    if card is Cards.LIBERAL:
        return
    l_remaining = deck[0]
    f_remaining = deck[1]
    tot_remaining = l_remaining + f_remaining

    prob_fff = multi_3(f_remaining)/multi_3(tot_remaining)
    prob_ffl = 3*l_remaining*multi_2(f_remaining)/multi_3(tot_remaining)
    prob_fll = 3*f_remaining*multi_2(l_remaining)/multi_3(tot_remaining)
    prob_cf = player.probabilities[president][0]
    prob_pf = player.probabilities[chancellor][0]

    prob_f = (prob_fff + prob_ffl*(prob_cf+prob_pf-prob_cf*prob_pf) + prob_fll*prob_cf*prob_pf)
    # prob_f = (prob_fff + prob_ffl*(prob_cf+prob_pf) + prob_fll*prob_cf*prob_pf)

    prob_president = (prob_fff*prob_pf + prob_ffl*(prob_pf) + prob_fll*prob_cf*prob_pf)
    prob_president /= prob_f
    player.set_prob(president, prob_president**.5)

    prob_chancellor = (prob_fff*prob_cf + prob_ffl*(prob_cf) + prob_fll*prob_cf*prob_pf)
    prob_chancellor /= prob_f
    player.set_prob(chancellor, prob_chancellor**.5)

    message = "Player {} analyzed new fascist policy enacted by president {} and chancellor {}"
    print(message.format(player.name, president, chancellor))
    player.print_probs()


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
