import argparse
import cProfile

from set_strats import *
from secret_hitler_ai.role import Role
from secret_hitler_ai.board import BoardStates
from secret_hitler_ai.game import Game
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
args = parser.parse_args()


def main():

    games = 1000
    Log.can_log = False
    for num_players in range(5, 11):
            f_wins = 0
            l_wins = 0
            f_policies = 0
            l_policies = 0
            h_shot = 0
            h_chanc = 0
            total_anarchies = 0

            for i in range(games):
                game = Game(num_players, True)
                for name, player in game.players.items():
                    if player.role is Role.LIBERAL:
                        set_liberal_strats(player, p_cards=args.LCPC)
                    elif player.role is Role.FASCIST:
                        set_fascist_strats(player, choose_c=args.FCC)
                    elif player.role is Role.HITLER:
                        set_hitler_strats(player, choose_c=args.HCC, p_cards=args.HCPC,
                                          c_cards=args.HCCC, vote=args.HV)

                winner, fascist_board, liberal_board, anarchies = game.run()

                total_anarchies += anarchies
                f_policies += fascist_board
                l_policies += liberal_board
                if winner is BoardStates.LIBERAL_WIN:
                    l_wins += 1
                elif winner is BoardStates.FASCIST_WIN:
                    f_wins += 1
                elif winner is BoardStates.HITLER_CHANCELLOR:
                    f_wins += 1
                    h_chanc += 1
                elif winner is BoardStates.HITLER_SHOT:
                    l_wins += 1
                    h_shot += 1


if __name__ == '__main__':
    cProfile.run('main()', 'results.cprof')

