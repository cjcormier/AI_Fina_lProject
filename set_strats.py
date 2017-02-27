from src.strategies import *


def set_liberal_strats(player):
    player.set_strategy(StrategyTypes.CHOOSE_CHANCELLOR, choose_liberal_chancellor)
    player.set_strategy(StrategyTypes.CHANCELLOR_CARDS, chancellor_choose_liberal_cards)
    player.set_strategy(StrategyTypes.PRESIDENT_CARDS, president_choose_liberal_cards())
    player.set_strategy(StrategyTypes.VOTE, standard_liberal_vote)
    player.set_strategy(StrategyTypes.ANALYZE_REVEALED_CARD, analyze_revealed_card)
    player.set_strategy(StrategyTypes.ANALYZE_CHANCELLOR_CARD, analyze_chancellor_card)


def set_fascist_strats(player):
    player.set_strategy(StrategyTypes.CHOOSE_CHANCELLOR, f_choose_liberal_chancellor)
    player.set_strategy(StrategyTypes.CHANCELLOR_CARDS, chancellor_choose_fascist_cards)
    player.set_strategy(StrategyTypes.PRESIDENT_CARDS, president_choose_fascist_cards)
    player.set_strategy(StrategyTypes.VOTE, standard_fascist_vote)
    player.set_strategy(StrategyTypes.ANALYZE_REVEALED_CARD, pass_strat)
    player.set_strategy(StrategyTypes.ANALYZE_CHANCELLOR_CARD, analyze_chancellor_card)


def set_hitler_strats(player):
    player.set_strategy(StrategyTypes.CHOOSE_CHANCELLOR, choose_liberal_chancellor)
    player.set_strategy(StrategyTypes.CHANCELLOR_CARDS, chancellor_choose_fascist_cards)
    player.set_strategy(StrategyTypes.PRESIDENT_CARDS, president_choose_fascist_cards)
    player.set_strategy(StrategyTypes.VOTE, standard_liberal_vote)
    player.set_strategy(StrategyTypes.ANALYZE_REVEALED_CARD, analyze_revealed_card)
    player.set_strategy(StrategyTypes.ANALYZE_CHANCELLOR_CARD, analyze_chancellor_card)