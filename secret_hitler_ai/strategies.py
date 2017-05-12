import random
from enum import Enum, unique

from secret_hitler_ai.cards import Cards
from secret_hitler_ai.roles import Role
from secret_hitler_ai.logging import Log


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
    assert player.name not in valid_players
    min_prob = 1
    players = []
    probabilities = player.probabilities
    for curr_player in valid_players:
        prob = probabilities[curr_player][0]
        if prob < min_prob:
            min_prob = prob
            players = [curr_player]
        elif prob == min_prob:
            players.append(curr_player)
    choices = players if len(players) > 0 else valid_players
    return random.choice(choices)


def choose_fascist_chancellor(player, valid_players):
    probabilities = player.probabilities
    fascist_players = []
    for valid_player in valid_players:
        if probabilities[valid_player][0] == 1:
            fascist_players.append(valid_player)
    if len(fascist_players) == 0:
        return choose_liberal_chancellor(player, valid_players)
    return random.choice(fascist_players)


def h_choose_fascist_chancellor(player, valid_players):
    max_prob = 0
    players = []
    probabilities = player.probabilities
    for valid_player in valid_players:
        prob = probabilities[valid_player][0]
        if prob > max_prob:
            max_prob = prob
            players = [valid_player]
        elif prob == max_prob:
            players.append(valid_player)
    players = players if len(players) > 0 else valid_players
    return random.choice(players)


def choose_not_hitler_chancellor(curr_player, valid_players):
    probabilities = curr_player.probabilities
    fascist_players = []

    for curr_player in valid_players:
        if curr_player in probabilities:
            if probabilities[curr_player][1] != 1:
                fascist_players.append(curr_player)
    choices = fascist_players if len(fascist_players) > 0 else valid_players
    return random.choice(choices)


def president_choose_liberal_cards(player, chancellor, cards):
    if Cards.FASCIST in cards:
        cards.remove(Cards.FASCIST)
    else:
        random.shuffle(cards)
        cards.pop()
    return cards


def president_give_choice(player, chancellor, cards):
    if Cards.LIBERAL in cards:
        if Cards.FASCIST in cards:
            cards = [Cards.LIBERAL, Cards.FASCIST]
            return cards
    random.shuffle(cards)
    cards.pop()
    return cards


def president_choose_fascist_cards(player, chancellor, cards):
    if Cards.LIBERAL in cards:
        cards.remove(Cards.LIBERAL)
    else:
        random.shuffle(cards)
        cards.pop()
    return cards


def chancellor_choose_liberal_cards(player, president, cards, deck):
    l_remaining = deck[0]
    f_remaining = deck[1]
    tot_remaining = l_remaining + f_remaining

    prob_fff = multi_3(f_remaining) / multi_3(tot_remaining)
    prob_ffl = 3 * l_remaining * multi_2(f_remaining) / multi_3(tot_remaining)
    prob_fll = 3 * f_remaining * multi_2(l_remaining) / multi_3(tot_remaining)
    prob_lll = multi_3(l_remaining) / multi_3(tot_remaining)
    default_fp = default_prob(player)
    default_lp = 1 - default_fp
    old_fp = player.probabilities[president][0]
    if Cards.LIBERAL in cards:
        card = Cards.LIBERAL
        cards.pop()
        if Cards.LIBERAL in cards:
            new_prob = 1 - (prob_lll+prob_fll)*default_lp/(prob_lll+prob_fll*default_lp)
            message = 'Chancellor {} is adjusting prob for player {} due to receiving 2 Liberal Cards'
        else:
            new_prob = (prob_fll*default_fp)/(prob_ffl*default_lp+prob_fll*default_fp)
            message = 'Chancellor {} is adjusting prob for player {} due to receiving 1 Liberal Card' \
                      'and 1 Fascist Card'
    else:
        new_prob = 1 - (prob_fff+prob_ffl)*default_fp/(prob_fff+prob_ffl*default_fp)
        message = 'Chancellor {} is adjusting prob for player {} due to receiving 2 Fascist Cards'
        card = Cards.FASCIST
        # player.print_probs()

    new_prob = rbe_markov_analysis(new_prob, old_fp, default_fp)
    player.set_prob(president, new_prob)
    Log.log_probs(message.format(player.name, president))
    return card


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
    if unknown_fascists == 0:
        default_individual_prob = 0
    else:
        default_individual_prob = unknown_fascists/unknown_players
    limit_prob = 2*default_individual_prob-default_individual_prob**2
    return president_prob+chancellor_prob-(president_prob*chancellor_prob) < limit_prob+.07


def standard_fascist_vote(player, president, chancellor):
    fascist_pres = president in player.fascists
    chancellor_pres = chancellor in player.fascists

    return fascist_pres or chancellor_pres


def analyze_revealed_card(player, president, chancellor, card, deck):
    l_remaining = deck[0]
    f_remaining = deck[1]
    tot_remaining = l_remaining + f_remaining
    tot_remaining_3 = multi_3(tot_remaining)
    prob_fff = multi_3(f_remaining)/tot_remaining_3
    prob_ffl = 3*l_remaining*multi_2(f_remaining)/tot_remaining_3
    prob_fll = 3*f_remaining*multi_2(l_remaining)/tot_remaining_3
    prob_lll = multi_3(l_remaining)/tot_remaining_3
    orig_prob = default_prob(player)
    prob_cf = orig_prob
    prob_pf = orig_prob
    prob_cl = 1 - prob_cf
    prob_pl = 1 - prob_pf
    prev_pf = player.probabilities[president][0]
    prev_cf = player.probabilities[chancellor][0]
    prob_president = 0.0
    prob_chancellor = 0.0

    if card is Cards.LIBERAL:
        if prob_lll == 0:
            if prob_pl == 0:
                prob_chancellor = 1.0
                prob_president = 0.0
            elif prob_cl == 0:
                prob_president = 1.0
                prob_chancellor = 0.0
            elif prob_cf == 0 and prob_pl == 0:
                prob_president = 0.0
                prob_chancellor = 0.0
        else:
            prob_l = prob_lll + prob_fll*(prob_cl+prob_pl-prob_cl*prob_pl) + \
                     prob_ffl*prob_cl*prob_pl
            prob_president = (prob_lll + prob_fll + prob_ffl*prob_cl)*prob_pl
            prob_president /= prob_l
            prob_president = 1-prob_president

            prob_chancellor = (prob_lll + prob_fll + prob_ffl*prob_pl)*prob_cl
            prob_chancellor /= prob_l
            prob_chancellor = 1-prob_chancellor
    else:
        prob_f = prob_fff + prob_ffl*(prob_cf+prob_pf-prob_cf*prob_pf) + prob_fll*prob_cf*prob_pf
        prob_president = (prob_fff+prob_ffl+prob_fll*prob_cf) * prob_pf
        prob_president /= prob_f
        prob_chancellor = (prob_fff+prob_ffl+prob_fll*prob_pf) * prob_cf
        prob_chancellor /= prob_f

    prob_president = rbe_markov_analysis(prob_president, prev_pf, orig_prob)
    prob_chancellor = rbe_markov_analysis(prob_chancellor, prev_cf, orig_prob)

    player.set_prob(president, prob_president)
    player.set_prob(chancellor, prob_chancellor)

    message = "Player {} analyzed new fascist policy enacted by president {} and chancellor {}"
    Log.log_probs(message.format(player.name, president, chancellor))
    # player.print_probs()


def rbe_markov_analysis(inv_sensor_model: float, recursive_term: float, prior: float)->float:
    if inv_sensor_model == 1 or recursive_term == 1:
        return inv_sensor_model
    gama_result = gama(inv_sensor_model, recursive_term, prior)
    return 1/(1+1/gama_result) if gama_result != 0 else 0


def gama(inv_sensor_model: float, recursive_term: float, prior: float)->float:
    return single_gama(inv_sensor_model) * single_gama(recursive_term) * single_gama(prior)


def single_gama(x: float)->float:
    return x/(1-x)


def default_prob(player):
    probabilities = player.probabilities
    unknown_fascists = player.num_fascists - len(player.fascists)
    unknown_players = len(set(probabilities.keys())-set(player.fascists)-{player.name})
    return unknown_fascists/unknown_players


def analyze_chancellor_card(player, chancellor, pres_cards, chanc_card):
    if chanc_card == Cards.FASCIST and Cards.LIBERAL in pres_cards:
        message = "Player {} thinks chancellor {} is a Fascist because they were given a " \
                  "choice and played a fascist policy."
        Log.log(message.format(player.name, chancellor))
        known_roles = {Role.FASCIST: player.fascists, Role.HITLER: player.hitler}
        if chancellor not in known_roles[Role.FASCIST]:
            known_roles[Role.FASCIST].append(chancellor)

        player.known_roles = known_roles
        player.set_prob(chancellor, 1)


def liberal_shoot(player, valid_players):
    return player.max_fascist(valid_players)


def fascist_shoot(player, valid_players):
    liberal_players = [x for x in valid_players if x not in player.fascists
                       and x is not player.hitler]
    return random.choice(liberal_players)


def hitler_shoot(player, valid_players):
    return player.min_fascist(valid_players)


def pass_strat(*args):
    pass


def random_choose_chancellor(player, valid_players):
    return random.choice(valid_players)


def random_president_cards(player, chancellor, cards):
    random.shuffle(cards)
    cards.pop()
    return cards


def random_chancellor_cards(player, president, cards, deck):
    random.shuffle(cards)
    cards.pop()
    return cards[0]


def vote_true(player, president, chancellor):
    return True


def shoot_random(player, valid_players):
    return random.choice(valid_players)

__all__ = ['StrategyTypes', 'choose_liberal_chancellor', 'choose_fascist_chancellor',
           'h_choose_fascist_chancellor', 'choose_not_hitler_chancellor',
           'president_choose_liberal_cards', 'president_give_choice',
           'president_choose_fascist_cards', 'chancellor_choose_liberal_cards',
           'chancellor_choose_fascist_cards', 'standard_liberal_vote', 'standard_fascist_vote',
           'analyze_revealed_card', 'analyze_chancellor_card',
           'liberal_shoot', 'fascist_shoot', 'hitler_shoot', 'pass_strat',
           'random_choose_chancellor', 'random_president_cards', 'random_chancellor_cards',
           'vote_true', 'shoot_random']
