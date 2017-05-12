import argparse

from set_strats import *
from secret_hitler_ai.game import Game
from secret_hitler_ai.roles import Role
from secret_hitler_ai.logging import Log

parser = argparse.ArgumentParser(description='AI Final Project Secret Hitler')
parser.add_argument('-LCPC', help='Strategy for Liberal choosing president cards.',
                    type=int, default=0)
parser.add_argument('-FCC', help='Strategy for Fascist to choose their chancellor.',
                    type=int, default=0)
parser.add_argument('-HCC', help='Strategy for Hitler to choose their chancellor.',
                    type=int, default=0)
parser.add_argument('-HCPC', help='Strategy for Hitler choosing president cards.',
                    type=int, default=0)
parser.add_argument('-HCCC', help='Strategy for Hitler choosing chancellor cards.',
                    type=int, default=0)
parser.add_argument('-HV', help='Strategy for Hitler voting on governments.',
                    type=int, default=0)
parser.add_argument('-v', help='Print Probabilities when they are updated',
                    type=bool, default=False)
parser.add_argument('-p', help='number of players',
                    type=int, default=8)
args = parser.parse_args()


def main():
    Log.allow_prob_logging(args.v)
    game = Game(args.p, True)

    for name, player in game.players.items():
        if player.role is Role.LIBERAL:
            set_liberal_strats(player, p_cards=args.LCPC)
        elif player.role is Role.FASCIST:
            set_fascist_strats(player, choose_c=args.FCC)
        elif player.role is Role.HITLER:
            set_hitler_strats(player, choose_c=args.HCC, p_cards=args.HCPC,
                              c_cards=args.HCCC, vote=args.HV)

    winner, fascist_board, liberal_board, anarchies = game.run()

    Log.log('')
    Log.log(winner)
    Log.log("Fascist Policies: {}, Liberal Policies: {}".format(fascist_board, liberal_board))


if __name__ == '__main__':
    main()
