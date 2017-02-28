from set_strats import *
from src.game import assign_roles, game
from src.strategies import set_adjust_factor
from src.roles import Role


def main():

    num_players = 8
    set_adjust_factor(1)
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


if __name__ == '__main__':
    main()
