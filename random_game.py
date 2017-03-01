from set_strats import *
from src.game import assign_roles, game
from src.strategies import set_adjust_factor
from src.roles import Role
from src.logging import Log


def main():

    num_players = 8
    set_adjust_factor(.2)
    players = assign_roles(num_players)
    for name, player in players.items():
        if player.role is Role.LIBERAL:
            set_liberal_strats(player)
        elif player.role is Role.FASCIST:
            set_fascist_strats(player)
        elif player.role is Role.HITLER:
            set_hitler_strats(player)

    winner, fascist_board, liberal_board, anarchies= game(num_players, players, allow_shoots=True)
    Log.log('')
    Log.log(winner)
    Log.log("Fascist Policies: {}, Liberal Policies: {}".format(fascist_board, liberal_board))


if __name__ == '__main__':
    main()
