import argparse

from set_strats import *
from secret_hitler_ai.roles import Role
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

    games = 10000

    header = 'Players,Games,Liberal wins,Fascist wins,HC wins,HS wins,L Policies,' \
             'F Policies,Total Policies,Average Anarchies'
    message = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}'
    Log.log(header)

    for num_players in range(5, 11):
            f_wins = 0
            l_wins = 0
            f_policies = 0
            l_policies = 0
            h_shot = 0
            h_chanc = 0
            total_anarchies = 0

            Log.allow_logging(False)
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
            Log.allow_logging(True)
            Log.log(message.format(num_players, games, l_wins, f_wins, h_chanc, h_shot,
                                   l_policies, f_policies, l_policies + f_policies,
                                   total_anarchies / games))


if __name__ == '__main__':
    main()
