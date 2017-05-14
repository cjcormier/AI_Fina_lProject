from set_strats import *
from secret_hitler_ai.role import Role
from secret_hitler_ai.board import BoardStates
from secret_hitler_ai.game import Game
from secret_hitler_ai.logging import Log


def main():
    games = 1000
    header = 'Players,Games,Liberal wins,Fascist wins,HC wins,HS wins,L Policies, F Policies,' \
             'Total Policies,Average Anarchies,FCC,HCC,LCPC,HCPC,HCCC,HV'
    message = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15}'

    # for n in range(0, 31, 2):
    Log.log(header)
    for num_players in range(5, 11):
        for fcc in range(len(f_choose_chancellor)):
            for hcc in range(len(h_choose_chancellor)):
                for lcpc in range(len(l_choose_p_cards)):
                    for hcpc in range(len(h_choose_p_cards)):
                        for hccc in range(len(h_choose_c_cards)):
                            for hv in range(len(h_vote)):

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
                                            set_liberal_strats(player, p_cards=lcpc)
                                        elif player.role is Role.FASCIST:
                                            set_fascist_strats(player, choose_c=fcc)
                                        elif player.role is Role.HITLER:
                                            set_hitler_strats(player, choose_c=hcc, p_cards=hcpc,
                                                              c_cards=hccc, vote=hv)

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
                                Log.log(message.format(num_players, games, l_wins, f_wins, h_chanc,
                                                       h_shot, l_policies, f_policies,
                                                       l_policies+f_policies, total_anarchies/games,
                                                       fcc, hcc, lcpc, hcpc, hccc, hv))


if __name__ == '__main__':
    main()
