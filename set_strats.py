from src.strategies import *

l_choose_chancellor = [
    choose_liberal_chancellor
]

f_choose_chancellor = [
    choose_fascist_chancellor,
    choose_liberal_chancellor,
    choose_not_hitler_chancellor
]

h_choose_chancellor = [
    h_choose_fascist_chancellor,
    choose_liberal_chancellor
]

l_choose_p_cards = [
    president_choose_liberal_cards,
    president_give_choice
]

f_choose_p_cards = [
    president_choose_fascist_cards
]

h_choose_p_cards = [
    president_choose_fascist_cards,
    president_choose_liberal_cards
]

l_choose_c_cards = [
    chancellor_choose_liberal_cards
]

f_choose_c_cards = [
    chancellor_choose_fascist_cards
]

h_choose_c_cards = [
    chancellor_choose_fascist_cards,
    chancellor_choose_liberal_cards
]

l_vote = [
    standard_liberal_vote
]

f_vote = [
    standard_fascist_vote
]

h_vote = [
    standard_fascist_vote,
    standard_liberal_vote
]

l_shoot = [
    liberal_shoot
]

f_shoot = [
    fascist_shoot
]

h_shoot = [
    fascist_shoot
]

l_strats = [l_choose_chancellor, l_choose_p_cards, l_choose_c_cards, l_vote, l_shoot]
f_strats = [f_choose_chancellor, f_choose_p_cards, f_choose_c_cards, f_vote, f_shoot]
h_strats = [h_choose_chancellor, h_choose_p_cards, h_choose_c_cards, h_vote, h_shoot]


def set_liberal_strats(player, choose_c=0, p_cards=0, c_cards=0, vote=0, shoot=0):
    player.set_strategy(StrategyTypes.CHOOSE_CHANCELLOR, l_choose_chancellor[choose_c])
    player.set_strategy(StrategyTypes.CHANCELLOR_CARDS, l_choose_c_cards[c_cards])
    player.set_strategy(StrategyTypes.PRESIDENT_CARDS, l_choose_p_cards[p_cards])
    player.set_strategy(StrategyTypes.VOTE, l_vote[vote])
    player.set_strategy(StrategyTypes.ANALYZE_REVEALED_CARD, analyze_revealed_card)
    player.set_strategy(StrategyTypes.ANALYZE_CHANCELLOR_CARD, analyze_chancellor_card)
    player.set_strategy(StrategyTypes.SHOOT, l_shoot[shoot])


def set_fascist_strats(player, choose_c=0, p_cards=0, c_cards=0, vote=0, shoot=0):
    player.set_strategy(StrategyTypes.CHOOSE_CHANCELLOR, f_choose_chancellor[choose_c])
    player.set_strategy(StrategyTypes.CHANCELLOR_CARDS, f_choose_c_cards[c_cards])
    player.set_strategy(StrategyTypes.PRESIDENT_CARDS, f_choose_p_cards[p_cards])
    player.set_strategy(StrategyTypes.VOTE, f_vote[vote])
    player.set_strategy(StrategyTypes.ANALYZE_REVEALED_CARD, pass_strat)
    player.set_strategy(StrategyTypes.ANALYZE_CHANCELLOR_CARD, analyze_chancellor_card)
    player.set_strategy(StrategyTypes.SHOOT, f_shoot[shoot])


def set_hitler_strats(player, choose_c=0, p_cards=0, c_cards=0, vote=0, shoot=0):
    player.set_strategy(StrategyTypes.CHOOSE_CHANCELLOR, h_choose_chancellor[choose_c])
    player.set_strategy(StrategyTypes.CHANCELLOR_CARDS, h_choose_c_cards[c_cards])
    player.set_strategy(StrategyTypes.PRESIDENT_CARDS, h_choose_p_cards[p_cards])
    player.set_strategy(StrategyTypes.VOTE, h_vote[vote])
    player.set_strategy(StrategyTypes.ANALYZE_REVEALED_CARD, analyze_revealed_card)
    player.set_strategy(StrategyTypes.ANALYZE_CHANCELLOR_CARD, analyze_chancellor_card)
    player.set_strategy(StrategyTypes.SHOOT, h_shoot[shoot])


def set_random(player):
    player.set_strategy(StrategyTypes.CHOOSE_CHANCELLOR, random_choose_chancellor)
    player.set_strategy(StrategyTypes.CHANCELLOR_CARDS, random_president_cards)
    player.set_strategy(StrategyTypes.PRESIDENT_CARDS, random_president_cards)
    player.set_strategy(StrategyTypes.VOTE, vote_true)
    player.set_strategy(StrategyTypes.ANALYZE_REVEALED_CARD, pass_strat)
    player.set_strategy(StrategyTypes.ANALYZE_CHANCELLOR_CARD, pass_strat)
    player.set_strategy(StrategyTypes.SHOOT, shoot_random)
