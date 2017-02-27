from src.game import assign_roles, game
from src.strategies import *


def main():

    num_players = 8
    players = assign_roles(num_players)
    for player in players:
        if player.role is Role.LIBERAL:
            set_liberal_strats(player)
        elif player.role is Role.FASCIST:
            set_fascist_strats(player)
        elif player.role is Role.HITLER:
            set_hitler_strats(player)

    winner, fascist_board, liberal_board, anarchies= game(num_players, players)
    print('')
    print(winner)
    print("Fascist Policies: {}, Liberal Policies: {}".format(fascist_board, liberal_board))


def set_liberal_strats(player):
    player.set_strategy(StrategyTypes.CHOOSE_CHANCELLOR, choose_liberal_chancellor)
    player.set_strategy(StrategyTypes.CHANCELLOR_CARDS, chancellor_choose_liberal_cards)
    player.set_strategy(StrategyTypes.PRESIDENT_CARDS, president_choose_liberal_cards)
    player.set_strategy(StrategyTypes.VOTE, standard_vote)
    player.set_strategy(StrategyTypes.ANALYZE_REVEALED_CARD, analyze_revealed_card)
    player.set_strategy(StrategyTypes.ANALYZE_CHANCELLOR_CARD, analyze_chancellor_card)


def set_fascist_strats(player):
    player.set_strategy(StrategyTypes.CHOOSE_CHANCELLOR, choose_fascist_chancellor)
    player.set_strategy(StrategyTypes.CHANCELLOR_CARDS, chancellor_choose_fascist_cards)
    player.set_strategy(StrategyTypes.PRESIDENT_CARDS, president_choose_fascist_cards)
    player.set_strategy(StrategyTypes.VOTE, standard_vote)
    player.set_strategy(StrategyTypes.ANALYZE_REVEALED_CARD, pass_strat)
    player.set_strategy(StrategyTypes.ANALYZE_CHANCELLOR_CARD, analyze_chancellor_card)


def set_hitler_strats(player):
    player.set_strategy(StrategyTypes.CHOOSE_CHANCELLOR, choose_fascist_chancellor)
    player.set_strategy(StrategyTypes.CHANCELLOR_CARDS, chancellor_choose_fascist_cards)
    player.set_strategy(StrategyTypes.PRESIDENT_CARDS, president_choose_fascist_cards)
    player.set_strategy(StrategyTypes.VOTE, standard_vote)
    player.set_strategy(StrategyTypes.ANALYZE_REVEALED_CARD, analyze_revealed_card)
    player.set_strategy(StrategyTypes.ANALYZE_CHANCELLOR_CARD, analyze_chancellor_card)


if __name__ == '__main__':
    main()
